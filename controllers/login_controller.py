from flask import render_template, request, flash, url_for, redirect
from ..forms.login_form import LoginForm
from ..models.models import ModelUser, User
from flask_login import login_user


def login_controller():
    form = LoginForm()
    if request.method == 'POST':
        user = User(email=request.form['email'], password=request.form['password'])
        logged_user = ModelUser.login(user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('index.index'))
            else: 
                flash('Invalid password')
                return render_template('auth/login.html', form=form)
        else: 
            flash('User Not Found')
            return render_template('auth/login.html', form=form)
    else:
        return render_template('auth/login.html', form=form)
