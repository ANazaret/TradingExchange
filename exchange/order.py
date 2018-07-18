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
            self._update_status(Status.FILLED)
        else:
            self._update_status(Status.PARTIAL)

    def cancel(self):
        self._update_status(Status.CANCELED)

    def _update_status(self, new_status: Status):
        self.status = new_status
        self.user.broadcast_order_update(self)

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
            'volume_remaining': self.volume_remaining,
            # other stuff to add
        }

    def set_id(self, n_orders):
        self.id = n_orders
