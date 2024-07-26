from flask import render_template
from flask_login import login_required
from app.account import account
from app.account.services import dashboard_service


@account.route('/dashboard')
@login_required
def dashboard():
    mastered_chars_count = dashboard_service.get_mastered_chars_count()
    return render_template('dashboard.html', title='Dashboard', mastered_chars_count=mastered_chars_count,)