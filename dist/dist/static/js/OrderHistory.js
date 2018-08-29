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

var OrderHistory = function () {
    function OrderHistory(selector, exchange_client) {
        _classCallCheck(this, OrderHistory);

        this.htmlObject = $(selector);
        this.htmlObject.append('<div class="list-group" style="margin-bottom: 0; overflow: auto"></div>');
        this.htmlObject = this.htmlObject.find('.list-group');
        this.htmlObject.height(exchange_client.order_book.htmlObject.find('table').height());
        this.orders = {};
    }

    _createClass(OrderHistory, [{
        key: 'update',
        value: function update(order, init) {
            if (!(order.id in this.orders)) {

                this.htmlObject.append('<a href="#" class="list-group-item"' + 'id="order_' + order.id + '" data-status="" ' + 'data-order-id="' + order.id + '" data-product-id="' + order.product_id + '">' + '<span class="order-side"></span> - ' + '<span class="order-price"></span>' + '  (<span class="order-volume"></span>) ' + '</a>');
                if (!init) {
                    this.scrollDown();
                }
            }
            this.orders[order.id] = order;
            var htmlOrder = this.htmlObject.find('#order_' + order.id);
            htmlOrder.find('.order-price').text(order.price);
            htmlOrder.find('.order-side').text(order.side == 'ask' ? "Sell" : "Buy");
            htmlOrder.find('.order-volume').text(order['volume_initial'] - order['volume_remaining'] + "/" + order["volume_initial"]);

            var color = void 0;
            switch (order.status) {
                case "FILLED":
                    color = "success";
                    break;
                case "PARTIAL":
                case "NEW":
                    color = "info";
                    break;
                case "CANCELED":
                    color = "danger";
            }
            color = "list-group-item-" + color;
            htmlOrder.removeClass("list-group-item-success").removeClass("list-group-item-info").removeClass("list-group-item-danger").addClass(color);

            htmlOrder.attr("data-status", order.status);
        }
    }, {
        key: 'scrollDown',
        value: function scrollDown() {
            var p = this.htmlObject;
            p.animate({ scrollTop: p.prop("scrollHeight") }, 400);
        }
    }]);

    return OrderHistory;
}();
//# sourceMappingURL=OrderHistory.js.map
//# sourceMappingURL=OrderHistory.js.map