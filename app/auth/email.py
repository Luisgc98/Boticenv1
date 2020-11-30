from flask import render_template, current_app
from flask_babel import _
from app.email import send_email

def send_registration_email(user):
    send_email(_('BOT·IC ')
                ,sender= current_app.config['ADMINS'][0]
                ,recipients=[user.email]
                ,text_body=render_template('email/successful_registration.txt', user=user)
                ,html_body=render_template('email/successful_registration.html',user=user))

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(_('BOT·IC Reset your password')
                ,sender= current_app.config['ADMINS'][0]
                ,recipients=[user.email]
                ,text_body=render_template('email/reset_password.txt'
                                            , user=user, token=token)
                ,html_body=render_template('email/reset_password.html'
                                            ,user=user, token=token))