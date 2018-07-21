from functools import wraps
from flask import render_template, session, Blueprint, request, redirect, url_for
from exchange.main import god

blueprint = Blueprint('views', __name__, template_folder='templates')


def username_required(func):
    @wraps(func)
    def aux(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('views.index'))
        return func(*args, **kwargs)

    return aux


def field_session_required(field):
    def decorator(func):
        @wraps(func)
        def aux(*args, **kwargs):
            if field not in session:
                return redirect(url_for('views.index'))
            return func(*args, **kwargs)

        return aux

    return decorator


@blueprint.route('/')
def index():
    if 'username' not in session:
        return render_template('login.html')
    return render_template('select_exchange.html', exchanges=god.exchanges)


@blueprint.route('/exchange/<string:exchange_id>')
@username_required
def exchange(exchange_id):
    if exchange_id not in god.exchanges:
        return redirect(url_for('views.index'))

    session['exchange_id'] = exchange_id

    return render_template('exchange_home.html', exchange=god.exchanges[exchange_id], depth=god.ORDER_BOOK_DEPTH)


@blueprint.route('/register/user/', methods=['POST'])
def register_user():
    user = god.register_user(request.form['username'])
    session['username'] = user.name
    session['user_id'] = user.id
    return redirect(url_for('views.index'))


@blueprint.route('/register/exchange/', methods=['POST'])
@username_required
def register_exchange():
    exchange_name = request.form['exchange_name']
    password = request.form['password']
    if exchange_name.lower().replace(' ', '') in [e.name.lower().replace(' ', '') for e in god.exchanges.values()]:
        return render_template('select_exchange.html', exchanges=god.exchanges, already_exists=True)

    god.register_exchange(exchange_name, password)

    return redirect(url_for('views.index'))


@blueprint.route('/logout/')
@username_required
def logout():
    del session['username']
    for k in ['user_id', 'exchange_id']:
        if k in session:
            del session[k]
    return redirect(url_for('views.index'))
