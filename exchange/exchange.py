from exchange.matchingEngine import MatchingEngine
from exchange.order import Order, Status
from exchange.orderBook import OrderBook
from exchange.product import Product


class Exchange:

    def __init__(self, name):
        self.name = name
        self.products = []
        self.order_books = dict()
        self.trades = dict()
        self.matching_engine = MatchingEngine()

    def add_product(self, name: str):
        for p in self.products:
            if p.name == name:
                return p

        product = Product(name, self)
        self.products.append(product)
        self.order_books[product] = OrderBook(product)
        self.trades[product] = []
        return product

    def place_order(self, order: Order):
        opposite_orders = self.order_books[order.product].get_opposite_queue(order)
        trades = self.matching_engine.match_order(order, opposite_orders)
        self.trades[order.product].extend(trades)
        if order.status in (Status.NEW | Status.PARTIAL):
            self.order_books[order.product].add_order(order)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()
