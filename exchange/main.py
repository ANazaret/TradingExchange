from exchange.exchange import Exchange
from exchange.user import User
import collections


class God:
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
        return exchange

    def register_user(self, name: str):
        for user_id in self.users:
            if self.users[user_id].name == name:
                return self.users[user_id]

        user = User(name)
        self.users[user.id] = user
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
