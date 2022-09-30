from flask import (
    render_template,
    session,
    redirect,
    url_for,
    request,
    jsonify
)
from bs4 import BeautifulSoup as BS
import requests
from . import main
from .. import db
from ..models import User


@main.route('/', methods=['GET'])
def index():
    context = {
        'useragent': request.headers.get('User-Agent'),
    }
    return render_template(
        '/pages/index.html',
        context=context,
        name=session.get('name'),
        known=session.get('known', False)
    )


@main.route('/tr-usd/')
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
