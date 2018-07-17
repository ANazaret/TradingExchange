import datetime
from enum import IntEnum, IntFlag
from exchange.product import Product


class Side(IntEnum):
    BID = 1
    ASK = 2

    @staticmethod
    def get_side(side_string: str):
        if side_string == 'ask':
            return Side.ASK
        if side_string == 'bid':
            return Side.BID
        raise Exception


class Status(IntFlag):
    CANCELED = 0
    NEW = 1
    PARTIAL = 2
    FILLED = 4


class Order:
    def __init__(self, user, side: Side, volume: int, price: float, product: Product):
        self.user = user
        self.side = side
        self.volume = volume
        self.volume_remaining = self.volume
        self.creation_time = datetime.datetime.now()
        self.price = price
        self.status = Status.NEW
        self.product = product
        self.id = None

    def trade(self, volume):
        self.volume_remaining -= volume

        if self.volume_remaining == 0:
            self.status = Status.FILLED
        else:
            self.status = Status.PARTIAL

    def cancel(self):
        self.status = Status.CANCELED

    def __str__(self):
        res = "(%s) %s %.2f (x %d/%d) %s on %s" % (
            self.status.name,
            "BUY" if self.side == Side.BID else "SELL",
            self.price,
            self.volume - self.volume_remaining,
            self.volume, self.product, self.product.exchange)
        return res

    def __repr__(self):
        return self.__str__()

    def json(self):
        return {
            'order_id': self.id,
            'status': self.status._name_,
            # other stuff to add
        }

    def set_id(self, n_orders):
        self.id = n_orders
