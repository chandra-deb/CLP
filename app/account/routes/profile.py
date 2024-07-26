from flask import render_template
from flask_login import current_user, login_required
from app.account import account


@account.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Profile', user=current_user)