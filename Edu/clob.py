from sortedcontainers import SortedList

from main import main
from position import position

# List-based representation of an order
# [timestamp, orderID, userID, contractID, price, side, qty]


class order_book:
    def __init__(self, _master: main, contract_information):
        self._master = _master

        self.contractID = int(contract_information["contract_id"])
        self.maxSettlement = contract_information["max_settlement"]
        self.marginFunction = [lambda x: x, lambda x: self.maxSettlement - x]

        self.accounts = _master.accounts

        self.book = [
            SortedList(key=lambda order: (-order[3], order[1])),
            SortedList(key=lambda order: (order[3], order[1])),
        ]

    def add_order(self, mpid, price, side, qty):
        if price < 1 or price >= self.maxSettlement or qty < 1 or (side not in [0, 1]):
            return False

        acct = self.accounts[mpid]
        acct_free_orders = acct.freeOrders
        if not len(acct.freeOrders):
            return False
        acct_positions = acct.positions
        new_position = self.contractID not in acct.positions
        if new_position:
            contract_pos = position(
                margin_function=self.marginFunction,
                balance=acct.balance,
                position=[0, 0],
            )
        else:
            contract_pos = acct_positions[self.contractID]

        if contract_pos.add_order(price=price, side=side, qty=qty):
            ctrparty_side = 1 - side
            ctrparty_book = self.book[ctrparty_side]
            can_fill = (
                (lambda maker_price: price >= maker_price)
                if side == 0
                else (lambda maker_price: maker_price >= price)
            )

            while True:
                if (not len(ctrparty_book)) or (not qty):
                    break
                ctrparty_order = ctrparty_book[0]
                ctrparty_mpid, ctrparty_price, ctrparty_qty = (
                    ctrparty_order[2],
                    ctrparty_order[4],
                    ctrparty_order[6],
                )
                if not can_fill(ctrparty_price):
                    break
                if mpid == ctrparty_mpid:
                    self.remove_order(ctrparty_order)
                    continue
                fill_qty = min(qty, ctrparty_qty)
                qty -= fill_qty
                ctrparty_qty -= fill_qty
                ctrparty_position = self.accounts[ctrparty_order[1]][self.contractID]
                ctrparty_position.fill_order(
                    ctrparty_price, ctrparty_side, ctrparty_price, fill_qty
                )
                if not ctrparty_qty:
                    self.remove_order(ctrparty_order, order_filled=True)
                    continue
                ctrparty_order[6] = ctrparty_qty

            if qty:
                new_order = [
                    self._master.eventID,
                    mpid,
                    self.contractID,
                    price,
                    side,
                    qty,
                ]
                new_order_id = acct_free_orders[-1]

    def remove_order(self, order, order_filled=False, ignore_book=False):
        order_id, order_mpid, order_price, order_side, order_qty = (
            order[1],
            order[2],
            order[4],
            order[5],
            order[6],
        )
        if not ignore_book:
            self.book[order_side].remove(order)

        order_acct = self.accounts[order_mpid]
        del order_acct.orders[order_id]

        if not order_filled:
            order_acct.positions[self.contractID].remove_order(
                order_price, order_side, order_qty
            )
