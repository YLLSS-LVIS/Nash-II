from contract_manager import contract_manager
from orders import orders
from sortedcontainers import SortedDict


class order_book:
    def __init__(self, _master, contract_id, max_settlement):
        self.accounts = _master.accounts
        self.orders: orders = _master.orders
        self.maxSettlement = int(max_settlement)
        self.margin_function = [lambda x: x, lambda x: self.maxSettlement - x]

        self.contractID = int(contract_id)
        self.books = [SortedDict(), SortedDict()]
        self.topOfBook = [None, None]

        self.contractManagers = {
            mpid: contract_manager(
                _account=account,
                margin_function=self.margin_function,
                position=account.positions[self.contractID],
                balance=account.balance,
            )
            for mpid, account in self.accounts.values()
            if self.contractID in account.positions
        }

        self.orderMPID = self.orders.mpid
        self.orderContract = self.orders.contract
        self.orderPrice = self.orders.price
        self.orderSide = self.orders.side
        self.orderQuantity = self.orders.quantity
        self.orderHead = self.orders.head
        self.orderTail = self.orders.tail
        self.orderUsed = self.orders.used

    def instantiate(self, contract_order_IDs: list):
        # contract_order_IDs is a list of existing alive orders which are related to the contract
        # this fuction does not have to be called if the system does not have an existing state to load (first boot)
        pass

    def post_order(self, mpid, price, side, qty):
        account_contract_manager = self.contractManagers.get(mpid)
        new_position = account_contract_manager is None
        if new_position:
            account = self.accounts.get(mpid)
            if account is None:
                return False, "The account does not exist"

            account_position = [0, 0]
            account_contract_manager = contract_manager(
                _account=account,
                margin_function=self.margin_function,
                position=account_position,
                balance=account.balance,
            )

        if account_contract_manager.add_order(price, side, qty):
            if new_position:
                self.contractManagers[mpid] = account_contract_manager
                account.positions[self.contractID] = account_position

            order_quantity = self.hit_book(price, 1 - side, qty, mpid)
            if not order_quantity:
                return True, "Order fully filled at entry"

            new_order_ID = self.orders.allocate_order()
            account_contract_manager.account.orders.add(new_order_ID)
            self.orderMPID[new_order_ID] = mpid
            self.orderContract[new_order_ID] = self.contractID
            self.orderPrice[new_order_ID] = price
            self.orderSide[new_order_ID] = side
            self.orderQuantity[new_order_ID] = order_quantity
            self.append_order(new_order_ID)
            return True

    def append_order(self):
        return

    def hit_book(self, price, side, qty, mpid=None, self_trade_prevention=True):
        self_trade = lambda x: x == mpid if self_trade_prevention else lambda x: False
        pass
