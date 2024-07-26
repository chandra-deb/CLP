from flask import Blueprint

#The blueprint name will require when using url_for function.
account: Blueprint = Blueprint('account', __name__, template_folder='templates', static_folder='static')

# Attach registered routes to this blueprint
from app.account.routes import *

