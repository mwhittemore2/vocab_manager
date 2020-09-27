from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from . import auth
from ..models import User
from .forms import LoginForm, RegistrationForm

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email=form.email.data
        first_name = form.first_name.data
        last_name= form.last_name.data
        password = form.password.data
        password_hash = generate_password_hash(password)
        user = User(email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password_hash=password_hash)
        user.save()
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_email = form.email.data
        user = User.objects(email=user_email).first()
        
        password = form.password.data
        is_correct_password = user.verify_password(password)
        if user is not None and is_correct_password:
            login_user(user)
            return redirect(url_for('content_management.select_content'))
        flash("Invalid username or password")
        
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))