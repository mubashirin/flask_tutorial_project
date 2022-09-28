from crypt import methods
import requests
from bs4 import BeautifulSoup as BS
from flask import (
    Flask,
    request,
    render_template,
    jsonify,
    url_for,
    flash,
    redirect
)
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = '40365aa1cefc0c9ab9dec43f191d4ac8851dd6653a6a2682'
moment = Moment(app)


class NewForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    context = {
        'useragent': request.headers.get('User-Agent'),
    }
    return render_template('/pages/index.html', context=context)


@app.route('/user/<name>/')
def user(name):
    return render_template('/pages/user.html', user=name)


@app.route('/tr-usd/')
def usd_tr():
    r = requests.get('https://www.kuveytturk.com.tr')
    html = BS(r.content, 'html.parser')
    
    t = html.find('table', {'class': 'table-market'}).find_all('em')
    
    data = {
        'bank': 'kuveytturk',
        'usd_tl': t[1].text.replace(',', '.'),
        'eur_tl': t[5].text.replace(',', '.'),
    }

    return jsonify(data)


@app.route('/create/', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        name = request.form['name']

        flash(f'Hello, {name.capitalize()}!')

    return render_template('/pages/create.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_page/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error_page/400.html'), 500


if __name__ == '__main__':
    app.run(debug=True, port=5077)
