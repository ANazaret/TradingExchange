from flask_socketio import emit

from exchange.exchange import Exchange
from exchange.user import User
import collections


class God:
    ORDER_BOOK_DEPTH = 6

    def __init__(self):
        self.exchanges = dict()
        self.users = dict()

        self.exchanges_id_counter = collections.defaultdict(int)

    def register_exchange(self, name: str, password: str = ""):
        for e_id in self.exchanges:
            if self.exchanges[e_id].name == name:
                return None
        exchange = Exchange(name, password)

        if self.exchanges_id_counter[exchange.id] > 0:
            exchange.id += "__%d" % (self.exchanges_id_counter[exchange.id])
        self.exchanges_id_counter[exchange.id] += 1
        self.exchanges[exchange.id] = exchange

        exchange.register_trades_subscriber(
            lambda x, y: emit('exchange_update', "Trade %s on %s" % (y.volume, x), room=x)
        )
        exchange.register_trades_subscriber(
            lambda x, y: print("Trade %s on %s" % (y.volume, x))
        )
        exchange.register_order_book_subscriber(
            lambda x, y: emit('book_update', {
                'product_id': y.product.id,
                'order_book': y.json(),
            }, room=x)
        )
        return exchange

    def register_user(self, name: str):
        for user_id in self.users:
            if self.users[user_id].name == name:
                return self.users[user_id]

        user = User(name)
        self.users[user.id] = user
        user.register_order_update_subscribers(
            lambda x, y: emit('order_update', y.json(), room=x)
        )
        return user

    def get_user(self, user_id: str) -> User:
        if user_id not in self.users:
            raise KeyError(user_id)
        return self.users[user_id]

    def get_exchange(self, exchange_id: str) -> Exchange:
        if exchange_id not in self.exchanges:
            raise KeyError(exchange_id)
        return self.exchanges[exchange_id]


god = God()
