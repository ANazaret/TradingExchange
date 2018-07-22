'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var OrderBook = function () {
    function OrderBook(selector, depth) {
        _classCallCheck(this, OrderBook);

        this.htmlObject = $(selector);
        this.depth = depth;
    }

    _createClass(OrderBook, [{
        key: 'update',
        value: function update(newBook) {
            this.book = newBook;
            this.update_side('bid');
            this.update_side('ask');
        }
    }, {
        key: 'update_side',
        value: function update_side(side) {
            for (var index = 0; index < this.depth; index++) {
                var cell = this.htmlObject.find('[data-side="' + side + '"][data-depth="' + index + '"]');
                var tmp = index < this.book[side].length ? this.book[side][index] : [' ', ' '];
                cell.find('.price').text(tmp[0]);
                cell.find('.volume-' + side).text(tmp[1]);
            }
        }
    }]);

    return OrderBook;
}();
//# sourceMappingURL=OrderBook.js.map