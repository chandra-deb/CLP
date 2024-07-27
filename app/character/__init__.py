from flask import Blueprint

#The blueprint name will require when using url_for function.
character: Blueprint = Blueprint('character', __name__, template_folder='templates', static_folder='static')

# Attach registered routes to this blueprint
from app.character.routes import *

