import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qwerty123458'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = "users.login"


from blog.core.views import core
from blog.users.views import users
from blog.posts.views import posts
from blog.tickets.views import tickets
from blog.error_pages.handlers import errors
app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(tickets)
app.register_blueprint(errors)