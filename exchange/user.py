from exchange.order import Order, Side
from exchange.product import Product


class User:
    def __init__(self, name: str):
        self.name = name
        self.orders = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def place_buy_order(self, price: float, volume: int, product: Product,) -> Order:
        return self.place_order(price, volume, product, Side.BID)

    def place_sell_order(self, price: float, volume: int, product: Product) -> Order:
        return self.place_order(price, volume, product, Side.ASK)

    def place_order(self, price: float, volume: int, product: Product, side : Side) -> Order:
        order = Order(self, side, volume, price, product)
        product.exchange.place_order(order)
        self.orders.append(order)

        return order.status
