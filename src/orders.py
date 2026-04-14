import array


class orders:
    def __init__(self, max_orders):
        init_enum = range(max_orders)
        self.free_orders = array.array("i", [i for i in init_enum])

        self.used = array.array("i", [0 for i in init_enum])
        self.mpid = array.array("i", [0 for i in init_enum])
        self.contract = array.array("i", [0 for i in init_enum])
        self.price = array.array("i", [0 for i in init_enum])
        self.side = array.array("i", [0 for i in init_enum])
        self.quantity = array.array("i", [0 for i in init_enum])
        self.head = array.array("i", [0 for i in init_enum])
        self.tail = array.array("i", [0 for i in init_enum])

        self.used_orders = 0

    def allocate_order(self):
        self.used[self.used_orders] = 1
        self.used_orders += 1
        return self.used_orders - 1

    def remove_order(self, order_id):
        if self.used[order_id] == 0:
            raise Exception("Attempted to kill a dead order")

        self.used[order_id] = 0
        self.used_orders -= 1
        self.free_orders[self.used_orders] = order_id
