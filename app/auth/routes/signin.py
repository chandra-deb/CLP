from flask import render_template
from app.auth import auth
from app.auth.forms.signin_form import SignInForm


@auth.route('/signin')
def signin():
    form = SignInForm()
    return render_template('signin.html', title='Sign In', form=form)