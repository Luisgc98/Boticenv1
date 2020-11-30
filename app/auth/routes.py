# Import the microframework to create web apps
import os
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.auth import bp
from app.auth.email import send_password_reset_email, send_registration_email
from app.auth.forms import LoginForm, RegisterForm, ResetPasswordRequestForm, ResetPasswordForm
from models import User, Address
from flask_babel import _

@bp.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if  user is None or not user.check_password(form.password.data):
            flash(_('Invalid email or password'))
            return redirect(url_for('auth.login'))
        login_user(user,remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if request.method =="POST" and form.validate_on_submit():
        #Verificando que el usuario aun no se haya registrado
        user = User.query.filter_by(email = form.email.data).first()
        if(user):
            flash(_("The email %(email)s is already in use"),email=form.email.data)
            return redirect(url_for('auth.register'))

        address= Address(city=form.city.data, state=form.state.data, municipality=form.municipality.data, 
        street= form.street.data, postal_code= form.postal_code.data, interior_number=form.interior_number.data, exterior_number=form.exterior_number.data )
        user= User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,addresses=[address])
        user.set_password(form.password.data)
        user.set_user_secret(form.email.data)
        db.session.add(user)
        db.session.commit()
        send_registration_email(user)
        flash(_("Congratulations you are a registered user, please confirm your email %(email)s!",email=form.email.data))
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@bp.route('/reset_password_request', methods=['GET','POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
            flash(_('Check your email for the instructions to reset your password'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',form=form)

@bp.route('/reset_password/<token>', methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)