from flask import render_template, session, Blueprint

blueprint = Blueprint('main', __name__, template_folder='templates')

@blueprint.route('/')
def index():
    return render_template('index.html')
