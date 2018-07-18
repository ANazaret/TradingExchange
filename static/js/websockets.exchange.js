
socket.on('connect', function() {
    $('h1').append(' - Connected');
    socket.emit('join_exchange', get_initial_exchange_data);
});

socket.on('exchange_update', function(data) {
    $('#exchange').append(data);
});

socket.on('order_update', function(data) {
    $('#exchange').append(data.order_id + " " + data.status);
});

function get_initial_exchange_data(){
    socket.emit(
        'get_initial_exchange_data',
        {'exchange_id': exchange_id, 'product_id':exchange_id+'__default'},
        function(data){
            console.log(data);
        })
}

function place_order(side, price, volume){
    socket.emit(
        'place_order',
        {'side': side,
         'price': price,
         'volume': volume,
         'product_id': product_id
        },
        function(data){
            console.log(data);
        }
    )
}

$('.btn-send-order').click( function(event){
    var side = event.originalEvent.target.attributes['data-side'].value;
    var price = parseFloat($('#price').val());
    var volume = parseInt($('#volume').val());
    if (price > 0 && volume > 0 ){
        place_order(side, price, volume);
    }
});
