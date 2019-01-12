
# modules and it's instances

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///site.db" #relative path for database
db = SQLAlchemy(app)  #SQLAlchemy database instance
bcrypt = Bcrypt(app)
login_manager = LoginManager(app) # it handles all the session in background after we add functionality in models
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from kktask import routes
