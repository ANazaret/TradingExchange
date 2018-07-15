from exchange.exchange import Exchange
from exchange.user import User
import collections


class God:
    def __init__(self):
        self.exchanges = dict()
        self.users = dict()

        self.exchanges_id_counter = collections.defaultdict(int)

    def register_exchange(self, name: str, password : str = ""):
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
        for user in self.users:
            if self.users[user].name == name:
                # raise Exception("Already registered")
                return None

        user = User(name)
        self.users[user.id] == user
        return user


god = God()
