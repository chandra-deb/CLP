from flask import render_template
from flask_login import current_user, login_required
# I did not choose:
# from app import account
# just to distinct between things directly coming from app package
# or from another package inside app package
from app.account import account


@account.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Profile', user=current_user)