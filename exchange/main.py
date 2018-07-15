from exchange.exchange import Exchange
from exchange.user import User


class God:
    def __init__(self):
        self.exchanges = dict()
        self.users = dict()

    def register_exchange(self, name: str):
        for e_id in self.exchanges:
            if self.exchanges[e_id].name == name:
                # raise Exception("Already registered")
                return None
        exchange = Exchange(name)
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
