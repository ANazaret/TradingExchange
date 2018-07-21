class OrderBook {

    constructor(selector, depth) {
        this.htmlObject = $(selector);
        this.depth = depth;
    }

    update(newBook) {
        this.book = newBook;
        this.update_side('bid');
        this.update_side('ask');
    }


    update_side(side) {
        for (var index = 0; index < this.depth; index++) {
            var cell = this.htmlObject.find('[data-side="' + side + '"][data-depth="' + index + '"]');
            var tmp = (index < this.book['order_book'][side].length) ?
                this.book['order_book'][side][index] : [' ', ' '];
            cell.find('.price').text(tmp[0]);
            cell.find('.volume-' + side).text(tmp[1]);
        }
    }
}
