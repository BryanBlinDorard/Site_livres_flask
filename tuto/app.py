from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import os.path
from flask_login import LoginManager


app = Flask(__name__)
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True


def mkpath(p):
  return os.path.normpath(os.path.join(os.path.dirname( __file__ ),p))

app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'+mkpath('../myapp.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.config['SECRET_KEY'] = '08fe1cdd-f8e1-4f5b-8945-6a244ae19e9f'

login_manager = LoginManager(app)
login_manager.login_view = 'login'