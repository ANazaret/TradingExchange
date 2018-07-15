class Product:
    def __init__(self, name: str, exchange):
        self.name = name
        self.exchange = exchange

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()
