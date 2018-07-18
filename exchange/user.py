from exchange.order import Order, Side
from exchange.product import Product
from exchange.utils import add_id


class User:
    @add_id('name')
    def __init__(self, name: str):
        self.name = name
        self.orders = []
        self.sid = None
        self.order_update_subscribers = []

        self.id = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def set_sid(self, sid: str):
        self.sid = sid

    def register_order_update_subscribers(self, subscriber):
        self.order_update_subscribers.append(subscriber)

    def broadcast_order_update(self, order):
        if not self.sid:
            return
        for f in self.order_update_subscribers:
            f(self.sid, order)

    def place_buy_order(self, price: float, volume: int, product: Product, ) -> Order:
        return self.place_order(price, volume, product, Side.BID)

    def place_sell_order(self, price: float, volume: int, product: Product) -> Order:
        return self.place_order(price, volume, product, Side.ASK)

    def place_order(self, price: float, volume: int, product: Product, side: Side) -> Order:
        order = Order(self, side, volume, price, product)
        product.exchange.place_order(order)
        self.orders.append(order)

        return order.status
