from flask import Flask, render_template, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from hanzipy.dictionary import HanziDictionary

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)


# dictionary = HanziDictionary()

from app import models

import hanzipy

# Here all the bluprint gets added to the main application
from app.auth import auth
app.register_blueprint(auth, url_prefix='/auth')

from app.account import account
app.register_blueprint(account)

from app.character import character
app.register_blueprint(character)



# from DictionaryDD.processed.processed_chars import word_list
# # from hanzipy.dictionary import HanziDictionary
#
# from app.models import ChineseCharacter
# with app.app_context():
#     dictionary = HanziDictionary()
#     for word in word_list:
#         print(word.encode('utf-8'))
#         try:
#             definitions = dictionary.definition_lookup(word)
#             for definition in definitions:
#                 simplified = definition['simplified']
#                 traditional = definition['traditional']
#                 pinyin = definition['pinyin']
#                 definition = definition['definition']
#
#                 char = ChineseCharacter(simplified=simplified, traditional=traditional,
#                                  pinyin=pinyin, definition=definition)
#                 db.session.add(char)
#         except KeyError:
#             pass
#     db.session.commit()



@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('account.dashboard'))
    return render_template('index.html')
