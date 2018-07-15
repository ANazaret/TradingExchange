from exchange.exchange import Exchange
from exchange.user import User


class God:
    def __init__(self):
        self.products = []
        self.exchanges = []
        self.users = []

    def register_exchange(self, name: str):
        constructor = Exchange
        field = self.exchanges

        for u in field:
            if u.name == name:
                # raise Exception("Already registered")
                return u

        obj = constructor(name)
        field.append(obj)
        return obj

    def register_user(self, name: str):
        constructor = User
        field = self.users

        for u in field:
            if u.name == name:
                # raise Exception("Already registered")
                return u

        obj = constructor(name)
        field.append(obj)
        return obj
