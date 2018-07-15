from exchange.order import Order, Side, Status
from exchange.orderQueue import OrderQueue
from exchange.trade import Trade


class MatchingEngine:

    def match_order(self, order: Order, opposite_orders: OrderQueue) -> list:
        negative_spread = (
            (lambda x, y: x.price > y.price) if order.side == Side.ASK else (lambda x, y: x.price < y.price)
        )
        buy_sell = (
            (lambda x, y: (x.user, y.user)) if order.side == Side.BID else (lambda x, y: (y.user, x.user))
        )
        trades = []

        while not opposite_orders.empty():
            if order.status == Status.FILLED:
                break
            if order.status == Status.CANCELED:
                return []

            opposite_order: Order = opposite_orders.get()
            if negative_spread(order, opposite_order):
                opposite_orders.put(opposite_order)
                break
            if opposite_order.status in (Status.CANCELED | Status.FILLED):
                continue

            price = (order.price + opposite_order.price) / 2
            volume = min(order.volume_remaining, opposite_order.volume_remaining)
            order.trade(volume)
            opposite_order.trade(volume)
            trades.append(Trade(volume, price, order.product, *buy_sell(order, opposite_order)))

            if opposite_order.status == Status.PARTIAL:
                opposite_orders.put(opposite_order)

        return trades
