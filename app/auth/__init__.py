from flask import Blueprint

#I am not sure yet what the name of the bluprint does...hehe
bp: Blueprint = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

# Attach registered routes to this blueprint
from app.auth.routes import *


