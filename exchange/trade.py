import datetime

from exchange.product import Product
from exchange.user import User


class Trade:
    def __init__(self, volume : int, price : float, product : Product, buyer : User, seller : User):
        self.product = product
        self.buyer = buyer
        self.seller = seller
        self.price = price
        self.volume = volume
        self.timestamp = datetime.datetime.now()

    def __str__(self):
        res = "(%s) %.2f (x %d) %s on %s" % (
            self.timestamp.isoformat(),
            self.price,
            self.volume, self.product, self.product.exchange)
        return res

    def __repr__(self):
        return self.__str__()