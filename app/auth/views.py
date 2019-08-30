from flask import render_template, redirect, url_for, flash
from . import auth
from ..models import User
from .forms import RegistrationForm

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email=form.email.data
        first_name = form.first_name.data
        last_name= form.last_name.data
        password = form.password.data
        user = User(email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password)
        user.save()
        flash('You can login now')
        #return redirect(url_for('auth.login'))
        return render_template('auth/login.html')
    return render_template('auth/register.html', form=form)