from flask import flash, redirect, url_for
from flask_login import logout_user

from app.auth import auth


@auth.route('/signout')
def signout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))
