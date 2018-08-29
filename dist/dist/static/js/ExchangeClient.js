'use strict';

var _createClass = function () {
    function defineProperties(target, props) {
        for (var i = 0; i < props.length; i++) {
            var descriptor = props[i];descriptor.enumerable = descriptor.enumerable || false;descriptor.configurable = true;if ("value" in descriptor) descriptor.writable = true;Object.defineProperty(target, descriptor.key, descriptor);
        }
    }return function (Constructor, protoProps, staticProps) {
        if (protoProps) defineProperties(Constructor.prototype, protoProps);if (staticProps) defineProperties(Constructor, staticProps);return Constructor;
    };
}();

function _classCallCheck(instance, Constructor) {
    if (!(instance instanceof Constructor)) {
        throw new TypeError("Cannot call a class as a function");
    }
}

var ExchangeClient = function () {
    function ExchangeClient(exchange_id, product_id, book_depth) {
        _classCallCheck(this, ExchangeClient);

        this.exchange_id = exchange_id;
        this.product_id = product_id;
        this.book_depth = book_depth;
        this.socket = io.connect('http://' + document.domain + ':' + location.port);
        this.order_book = new OrderBook('#order_book', this.book_depth);
        this.order_history = new OrderHistory("#order_history", this);
        this.bindSockets();
        this.bindEvents();
    }

    _createClass(ExchangeClient, [{
        key: 'bookUpdate',
        value: function bookUpdate(data) {
            this.order_book.update(data['order_book']);
        }
    }, {
        key: 'orderUpdate',
        value: function orderUpdate(data) {
            this.order_history.update(data);
        }
    }, {
        key: 'connect',
        value: function connect() {
            $('#exchange-name').append(' <span class="glyphicon glyphicon-ok"></span>');
            this.socket.emit('join_exchange', { 'exchange_id': this.exchange_id, 'product_id': this.exchange_id + '__default' }, this.initExchangeData.bind(this));
        }
    }, {
        key: 'initExchangeData',
        value: function initExchangeData(data) {
            var _this = this;

            this.order_book.update(data['order_book']);
            data['user_orders'].forEach(function (order) {
                return _this.order_history.update(order, true);
            });
            this.order_history.scrollDown();
        }
    }, {
        key: 'bindSockets',
        value: function bindSockets() {
            var self = this;
            this.socket.on('connect', function () {
                return self.socket.emit('connected', self.connect.bind(self));
            });
            this.socket.on('exchange_update', function () {
                return undefined;
            });
            this.socket.on('order_update', self.orderUpdate.bind(self));
            this.socket.on('book_update', self.bookUpdate.bind(self));
        }
    }, {
        key: 'bindEvents',
        value: function bindEvents() {
            var self = this;
            $('.btn-send-order').click(self.eventPlaceOrder.bind(self));
        }
    }, {
        key: 'eventPlaceOrder',
        value: function eventPlaceOrder(event) {
            var side = event.originalEvent.target.attributes['data-side'].value;
            var price = parseFloat($('#price').val());
            var volume = parseInt($('#volume').val());
            if (price > 0 && volume > 0) {
                this.placeOrder(side, price, volume);
            }
        }
    }, {
        key: 'placeOrder',
        value: function placeOrder(side, price, volume) {
            var _this2 = this;

            this.socket.emit('place_order', {
                'side': side,
                'price': price,
                'volume': volume,
                'product_id': this.product_id
            }, function (order) {
                return _this2.orderUpdate.bind(_this2)(order);
            });
        }
    }, {
        key: 'cancelOrder',
        value: function cancelOrder(order_id, product_id) {
            this.socket.emit('cancel_order', {
                'product_id': product_id,
                'order_id': order_id
            });
        }
    }], [{
        key: 'orderUpdate',
        value: function orderUpdate(order) {
            $('#exchange').append(order.order_id + " " + order.status);
        }
    }]);

    return ExchangeClient;
}();
//# sourceMappingURL=ExchangeClient.js.map
//# sourceMappingURL=ExchangeClient.js.map