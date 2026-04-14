from position import position


class account:
    __slots__ = []

    # List-based representation of an order
    # [timestamp, userID, contractID, price, side, qty]

    def __init__(self, max_orders):
        self.balance = [0, 0]
        self.orders = {}
        self.positions = {}
