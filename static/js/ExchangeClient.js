class ExchangeClient {
    constructor(exchange_id, product_id, book_depth) {
        this.exchange_id = exchange_id;
        this.product_id = product_id;
        this.book_depth = book_depth;
        this.socket = io.connect('http://' + document.domain + ':' + location.port);
        this.order_book = new OrderBook('#order_book', this.book_depth);
        this.bindSockets();
        this.bindEvents();
    }

    static orderUpdate(order) {
        $('#exchange').append(order.order_id + " " + order.status);
    }

    bookUpdate(book) {
        this.order_book.update(book);
    }

    connect() {
        $('#exchange-name').append(' <span class="glyphicon glyphicon-ok"></span>');
        this.socket.emit('join_exchange',
            {'exchange_id': this.exchange_id, 'product_id': this.exchange_id + '__default'},
            (book) => this.order_book.update(book));
    }

    bindSockets() {
        const self = this;
        this.socket.on('connect', () => self.socket.emit('connected', self.connect.bind(self)));
        this.socket.on('exchange_update', () => undefined);
        this.socket.on('order_update', ExchangeClient.orderUpdate);
        this.socket.on('book_update', self.bookUpdate.bind(self));
    }

    bindEvents() {
        const self = this;
        $('.btn-send-order').click(self.eventPlaceOrder.bind(self));
    }

    eventPlaceOrder(event) {
        let side = event.originalEvent.target.attributes['data-side'].value;
        let price = parseFloat($('#price').val());
        let volume = parseInt($('#volume').val());
        if (price > 0 && volume > 0) {
            this.place_order(side, price, volume);
        }
    }

    place_order(side, price, volume) {
        this.socket.emit('place_order', {
                'side': side,
                'price': price,
                'volume': volume,
                'product_id': this.product_id
            },
            (data) => console.log(data));
    }
}