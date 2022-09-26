import json
from unicodedata import decimal
import requests
from bs4 import BeautifulSoup as BS
from flask import (
    Flask,
    request,
    render_template,
    jsonify
)
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'itbfrdrweq34565iytctexsxt5789obf-te3wxt3s'
moment = Moment(app)


class NewForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NewForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''

    context = {
        'useragent': request.headers.get('User-Agent'),
        'name': name
    }
    return render_template('/pages/index.html', form=form, context=context)


@app.route('/user/<name>/')
def user(name):
    return render_template('/pages/user.html', user=name)


@app.route('/tr-usd/')
def usd_tr():
    r = requests.get('https://www.kuveytturk.com.tr')
    html = BS(r.content, 'html.parser')
    
    t = html.find('table', {'class': 'table-market'}).find_all('em')

    # print(float(t[1].text))
    
    data = {
        'bank': 'kuveytturk',
        'usd_tl': t[1].text,
        'eur_tl': t[5].text,
    }

    return jsonify(data)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_page/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error_page/400.html'), 500


if __name__ == '__main__':
    app.run(debug=True, port=5077)
