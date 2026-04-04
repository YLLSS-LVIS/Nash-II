from position import position

class account:
    __slots__ = []

    # List-based representation of an order
    # [timestamp, userID, contractID, price, side, qty]

    def __init__(self, max_orders):
        self.balance = [0, 0]
        self.orders = {}
        self.freeOrders = [i for i in range(max_orders)]
        self.positions = {}

    def add_order(self, contractID, contract_margin_function, price, side, qty):
        new_contract = contractID not in self.positions
        if new_contract:
            user_position = position(
