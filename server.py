from flask import Flask, render_template, session
from flask_socketio import SocketIO
from exchange.main import god
from views import blueprint

app = Flask(__name__)
app.register_blueprint(blueprint)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


god.register_exchange('Fish market')
god.register_exchange('Love Island', 'interns')

@socketio.on('client_connected')
def handle_message(message):
    print(message)


if __name__ == '__main__':
    socketio.run(app, port=8000, debug=True)
