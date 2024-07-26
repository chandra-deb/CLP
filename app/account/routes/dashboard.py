from flask import render_template
from flask_login import login_required
from app.account import account
from app.account.services import dashboard_service


@account.route('/dashboard')
@login_required
def dashboard():
    mastered_chars_count = dashboard_service.mastered_chars_len
    vocabulary_count = dashboard_service.vocabulary_len
    return render_template('dashboard.html', title='Dashboard', mastered_chars_count=mastered_chars_count,
                           vocabulary_count=vocabulary_count)
