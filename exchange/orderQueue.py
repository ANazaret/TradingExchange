from exchange.order import Side, Order


class OrderQueue:
    def __init__(self, side : Side):
        self._data = []
        if side == Side.BID:
            self.lt = lambda o1, o2 : (-o1.price, o1.creation_time) < (-o2.price, o2.creation_time)
        else:
            self.lt = lambda o1, o2 : (o1.price, o1.creation_time) < (o2.price, o2.creation_time)

    def __lt__(self, other):
        if self.side == Side.ASK:
            return (self.price, self.creation_time) < (other.price, other.creation_time)

        elif self.side == Side.BID:
            return
    def put(self, order : Order):
        index = -1
        for i,o in enumerate(self._data):
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
