from flask import render_template,request,redirect,url_for, flash
from app.auth import bp as auth_bp
from flask_login import current_user, login_user
from app.models import User
from app import db
from app.auth.forms.signup_form import SignUpForm


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)

        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)