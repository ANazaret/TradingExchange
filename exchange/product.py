from exchange.utils import add_id


class Product:
    @add_id('exchange_and_name')
    def __init__(self, name: str, exchange):
        self.name = name
        self.exchange = exchange
        self.exchange_and_name = exchange.name + '_' + name
        self.id = None

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()
