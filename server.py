from flask import Flask, render_template, session, request, Blueprint
from flask_socketio import SocketIO, join_room, emit
from exchange.main import god
from exchange.order import Side
from exchange.utils import check_dict_fields, check_data_errors
from views import blueprint, username_required, field_session_required

app = Flask(__name__)
app.register_blueprint(blueprint)
blueprint_dist = Blueprint('generated', __name__, static_url_path='/static/generated', static_folder='dist/static')
app.register_blueprint(blueprint_dist)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

god.register_exchange('Fish market')
god.register_exchange('Love Island', 'interns')
god.register_user('Achille')
god.register_user('Henry')


@socketio.on('connected')
def connection():
    session['sid'] = request.sid


@socketio.on('join_exchange')
def join_exchange(message):
    if not check_dict_fields(message, ['exchange_id', 'product_id']):
        return 'Invalid request'
    print(session['username'] + ' has joined ' + session['exchange_id'])
    join_room(session['exchange_id'])
    user = god.get_user(session['user_id'])
    user.set_sid(session['sid'])

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
    socketio.run(app, host="0.0.0.0", port=8000, debug=True)
