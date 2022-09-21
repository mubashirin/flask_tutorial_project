from flask import (
    Flask,
    request,
    render_template,
)
from flask_moment import Moment
from datetime import datetime


app = Flask(__name__)
moment = Moment(app)


@app.route('/')
def index():
    context = {
        'useragent': request.headers.get('User-Agent'),
    }
    return render_template('/pages/index.html', current_time=datetime.utcnow(), context=context)


@app.route('/user/<name>/')
def user(name):
    return render_template('/pages/user.html', user=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_page/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error_page/400.html'), 500


if __name__ == '__main__':
    app.run(debug=True, port=5077)
