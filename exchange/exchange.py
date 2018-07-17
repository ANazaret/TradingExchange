from exchange.matchingEngine import MatchingEngine
from exchange.order import Order, Status, Side
from exchange.orderBook import OrderBook
from exchange.product import Product
from exchange.user import User
from exchange.utils import add_id

class Exchange:
    @add_id('name')
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.products = dict()
        self.order_books = dict()
        self.trades = dict()
        self.matching_engine = MatchingEngine()
        self.id = None

        self.add_product('_default')
        self.n_orders = 0


    def add_product(self, name: str):
        for p in self.products.values():
            if p.name == name:
                return p

        product = Product(name, self)
        self.products[product.id] = product
        self.order_books[product.id] = OrderBook(product)
        self.trades[product.id] = []
        return product

    def place_order(self, user : User, product_id : str, side : Side, volume : int, price : float) -> Order:
        order = Order(user, side, volume, price, self.products[product_id])
        order.set_id(self.n_orders)
        self.n_orders += 1
        self._place_order(order)
        return order

    def _place_order(self, order: Order):
        opposite_orders = self.order_books[order.product.id].get_opposite_queue(order)
        trades = self.matching_engine.match_order(order, opposite_orders)
        self.trades[order.product.id].extend(trades)
        if order.status in (Status.NEW | Status.PARTIAL):
            self.order_books[order.product.id].add_order(order)


    def get_order_book(self, product_id : str) -> OrderBook:
        if product_id not in self.order_books:
            raise KeyError(product_id)
        return self.order_books[product_id]


    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()
