import os
import requests
from bs4 import BeautifulSoup as BS
from flask import (
    Flask,
    request,
    render_template,
    jsonify,
    url_for,
    flash,
    redirect,
    session
)
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_migrate import Migrate


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = '40365aa1cefc0c9ab9dec43f191d4ac8851dd6653a6a2682'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self) -> str:
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


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
        user = User.query.filter_by(username=name).first()
        if user is None:
            user = User(username=name)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        
        session['name'] = name

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
