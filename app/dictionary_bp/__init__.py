from flask import Blueprint

#The blueprint name will require when using url_for function.
character: Blueprint = Blueprint('dictionary', __name__, template_folder='templates', static_folder='static',
                                 url_prefix='/dictionary')

# Attach registered routes to this blueprint
from app.dictionary_bp.routes import *
# from app.character.apis import *
