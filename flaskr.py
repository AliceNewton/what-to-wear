# all the imports
from __future__ import with_statement
from os import environ
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
from urlparse import urlparse
import simplejson
import urllib2
import datetime


# configuration
DEBUG = True
SECRET_KEY = environ.get('SECRET_KEY', 'development')
USERNAME = 'admin'
PASSWORD = 'default'
APPKEY = 'a6d8eaaef8203121120909'
SQLALCHEMY_DATABASE_URI = 'sqlite:///data-new.db'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)


  outfit string not null,
  bottoms string not null,
  cover string not null,
  shoes string not null,
  rainproof boolean,
  smart boolean,
  lastworn string not null


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    outfit = db.Column(db.String(200))
    bottoms = db.Column(db.String(200))
    cover = db.Column(db.String(200))
    shoes = db.Column(db.String(200))
    rainproof = db.Column(db.Boolean())
    smart = db.Column(db.Boolean())
    lastworn = db.Column(db.String(200))

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username
        

def connect_db():
    """Returns a new connection to the database."""
    if POSTGRESQL_URL is not None:
        conn = dbadapter.connect(host=POSTGRESQL_HOST,
                                 port=POSTGRESQL_PORT,
                                 database=POSTGRESQL_DATABASE,
                                 user=POSTGRESQL_USER,
                                 password=POSTGRESQL_PASSWORD)
    else:
        conn = dbadapter.connect(app.config['DATABASE'])
    return conn


def init_db():
    """Creates the database tables."""
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


@app.before_request
def before_request():
    """Make sure we are connected to the database each request."""
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def home():
    return render_template('home.html', today = datetime.date.today())
    
@app.route('/hello')
def hello():
    return '{"message": "Hello world"}'
    
@app.route('/meetings')
def meetings():
	return render_template('meetingq.html', today = datetime.date.today())
    
@app.route('/weather', methods=['POST'])
def get_weather():
    # get weather information
    today = datetime.date.today()
    url = 'http://free.worldweatheronline.com/feed/weather.ashx?key=a6d8eaaef8203121120909&q=SW7&num_of_days=1&format=json'
    json = urllib2.urlopen(url).read()
    weatherdata = simplejson.loads(json)
    maxtemp = weatherdata['data']['weather'][0]['tempMaxC']
    maxtemp = int(maxtemp)
    weatherDesc = weatherdata['data']['weather'][0]['weatherDesc'][0]['value']
    raining = 1 if 'rain' in weatherDesc else 0
        
    # get calendar information
    qanswer = request.form['qanswer']
    smartmeeting = 1 if qanswer == 'Yes' else 0
    
    # pick outfit with appropriate criteria
    outfit = query_db("SELECT * FROM items WHERE rainproof=? AND smart=? AND DATE(lastworn) <= DATE('now', 'weekday 0', '-18 days')", (raining, smartmeeting))
    return render_template('outfit.html', **locals())

@app.route('/chosen', methods=['POST'])
def chosenoutfit():
    today = datetime.date.today()
    todayISO = today.strftime("%Y-%m-%d %H:%M:%S")
    outfitid = request.form['outfitid']
    g.db.execute("UPDATE items SET lastworn=? WHERE id=?", [todayISO, outfitid])
    g.db.commit()
    outfit = query_db("SELECT * FROM items WHERE id=?", [outfitid])
    return render_template('outfitchosen.html', **locals())
    
if __name__ == '__main__':
    port = int(environ.get('PORT', 5000))
    app.run(port=port, host='0.0.0.0')
    
