from flask import Flask, render_template, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from app import models

# Here all the bluprint gets added to the main application
from app.auth import auth
app.register_blueprint(auth, url_prefix='/auth')

from app.account import account
app.register_blueprint(account)

from app.character import character
app.register_blueprint(character)


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('account.dashboard'))
    return render_template('index.html')
