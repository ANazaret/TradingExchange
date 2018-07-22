class OrderHistory {
    constructor(selector, exchange_client) {
        this.htmlObject = $(selector);
        this.htmlObject.append('<div class="list-group" style="margin-bottom: 0; overflow: auto"></div>');
        this.htmlObject = this.htmlObject.find('.list-group');
        this.htmlObject.height(exchange_client.order_book.htmlObject.find('table').height());
        this.orders = {};
    }

    update(order, init) {
        if (!(order.id in this.orders)) {

            this.htmlObject.append(
                '<a href="#" class="list-group-item"' +
                'id="order_' + order.id + '" data-status="" ' +
                'data-order-id="' + order.id + '" data-product-id="' + order.product_id + '">' +
                '<span class="order-side"></span> - ' +
                '<span class="order-price"></span>' +
                '  (<span class="order-volume"></span>) ' +
                '</a>')
            if (!init) {
                this.scrollDown();
            }

        }
        this.orders[order.id] = order;
        let htmlOrder = this.htmlObject.find('#order_' + order.id);
        htmlOrder.find('.order-price').text(order.price);
        htmlOrder.find('.order-side').text((order.side == 'ask') ? "Sell" : "Buy");
        htmlOrder.find('.order-volume').text(
            (order['volume_initial'] - order['volume_remaining']) + "/" + order["volume_initial"]);

        let color;
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
        htmlOrder.removeClass("list-group-item-success")
            .removeClass("list-group-item-info")
            .removeClass("list-group-item-danger")
            .addClass(color);

        htmlOrder.attr("data-status", order.status);
    }

    scrollDown() {
        let p = this.htmlObject;
        p.animate({scrollTop: p.prop("scrollHeight")}, 400);
    }
}
