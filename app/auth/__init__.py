from flask import Blueprint

#The blueprint name will require when using url_for function.

auth: Blueprint = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

# Attach registered routes to this blueprint
from app.auth.routes import *


