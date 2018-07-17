
socket.on('connect', function() {
    $('h1').append(' - Connected');
    socket.emit('join_exchange', get_initial_exchange_data);
});

socket.on('exchange_update', function(data) {
    $('h1').append(data);
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