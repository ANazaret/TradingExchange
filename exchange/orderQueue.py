from exchange.order import Side, Order, Status


class OrderQueue:
    def __init__(self, side: Side):
        self._data = []
        if side == Side.BID:
            self.lt = lambda o1, o2: (-o1.price, o1.creation_time) < (-o2.price, o2.creation_time)
        else:
            self.lt = lambda o1, o2: (o1.price, o1.creation_time) < (o2.price, o2.creation_time)

    def put(self, order: Order):
        index = -1
        for i, o in enumerate(self._data):
            if self.lt(order, o):
                index = i
                break
        if index == -1:
            index = len(self._data)
        self._data.insert(index, order)

    def get(self) -> Order:
        return self._data.pop(0)

    def empty(self) -> bool:
        return len(self._data) == 0

    def clean(self):
        self._data = list(filter(lambda o: o.status in (Status.NEW | Status.PARTIAL), self._data ))

    def json(self):
        self.clean()
        # Functional style <3
        def aux(orders):
            if len(orders) == 0:
                return []
            order = orders[0]
            if len(orders) == 1:
                return [(order.price, order.volume_remaining)]
            res = aux(orders[1:])
            if res[0][0] == order.price:
                x = res.pop(0)
                res.insert(0, (order.price, x[1] + order.volume_remaining))
            else:
                res.insert(0, (order.price, order.volume_remaining))
            return res

        return aux(self._data)
