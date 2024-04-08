from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '367578e98c380c34fb10c60830d21bf2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site.db') 
db = SQLAlchemy(app)
bcrypt =  Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = 'info    '

from flask_blog import routes
