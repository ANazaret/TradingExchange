from flask import Flask, render_template, session
from flask_socketio import SocketIO, join_room, emit
from exchange.main import god
from exchange.order import Side
from exchange.utils import check_dict_fields, check_data_errors
from views import blueprint, username_required, field_session_required

app = Flask(__name__)
app.register_blueprint(blueprint)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

god.register_exchange('Fish market')
god.register_exchange('Love Island', 'interns')


@socketio.on('client_connected')
def handle_message(message):
    0  # print(message)


@socketio.on('join_exchange')
def join_exchange():
    if 'exchange_id' not in session:
        return
    print(session['username'] + ' has joined ' + session['exchange_id'])
    join_room(session['exchange_id'])


@socketio.on('get_initial_exchange_data')
@username_required
def get_initial_exchange_data(message):
    if not check_dict_fields(message, ['exchange_id', 'product_id']):
        return 'Invalid request'
    exchange_id = message['exchange_id']
    product_id = message['product_id']

    if exchange_id not in god.exchanges:
        return 'Invalid exchange_id'
    if product_id not in god.exchanges[exchange_id].products:
        return 'Invalid product_id for exchange %s' % exchange_id

    return {
        'order_book': god.get_exchange(exchange_id).get_order_book(product_id).json(),
    }


@socketio.on('place_order')
@username_required
@field_session_required(field='exchange_id')
def place_order(data):
    if not check_dict_fields(data, ['product_id', 'side', 'volume', 'price']):
        return 'Invalid request'

    if not check_data_errors(data):
        return 'Errors in fields'

    side = data['side']
    side = Side.get_side(side)
    volume = data['volume']
    price = data['price']
    product_id = data['product_id']
    exchange_id = session['exchange_id']
    user_id = session['user_id']
    order = god.get_exchange(exchange_id).place_order(
        god.get_user(user_id), product_id, side, volume, price)

    return {
        'order': order.json(),
    }


if __name__ == '__main__':
    socketio.run(app, port=8000, debug=True)
    while True:
        for e_id in god.exchanges:
            emit('exchange_update', 'Bite %s' % e_id, room=e_id, namespace='/')
        socketio.sleep(5)
