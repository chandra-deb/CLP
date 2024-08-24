from flask import Blueprint

#The blueprint name will require when using url_for function.
character: Blueprint = Blueprint('character', __name__, template_folder='templates', static_folder='static',
                                 url_prefix='/character')

# Attach registered routes to this blueprint
from app.character.routes import *
from app.character.apis import *
