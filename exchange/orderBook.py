from exchange.order import Order, Side
from exchange.orderQueue import OrderQueue
from exchange.product import Product

class OrderBook:
    def __init__(self, product : Product):
        self.product = product
        self.bid_queue = OrderQueue(Side.BID)
        self.ask_queue = OrderQueue(Side.ASK)

    def add_order(self, order: Order):
        if order.side == Side.BID:
            self.bid_queue.put(order)
        else:
            self.ask_queue.put(order)

    def get_opposite_queue(self, order : Order):
        if order.side == Side.BID:
            return self.ask_queue
        return self.bid_queue

    def __str__(self):
        res = ""





