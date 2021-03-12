import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)

app.secret_key = os.urandom(24)

app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = 'login'
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='773441350951-f8oqglmb4nkbjadj90h9lpqko4bleecm.apps.googleusercontent.com',
    client_secret='o5RXltUHXMEZAbgmPUQql2V_',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
)

twitter = oauth.register(
    name='twitter',
    client_id='Zb2caXDpFNyEReMYho6qEYFBU',
    client_secret='yGQv8qzfe9dayolMgtgaqMZAZw7rb3fM3Q62LyLdEvA0UblfJx',
    access_token_url='https://api.twitter.com/oauth/access_token',
    access_token_params=None,
    authorize_url='https://api.twitter.com/oauth/authenticate',
    authorize_params=None,
    api_base_url='https://api.twitter.com/1.1/',
    client_kwargs={'scope': 'openid email profile'},
    request_token_url='https://api.twitter.com/oauth/request_token',
)

from Dashboard import views, models
db.create_all()

@login.user_loader
def load_user(id):
    return models.User.query.get(id)

