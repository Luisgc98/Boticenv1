import logging
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange, EqualTo, ValidationError
from flask_babel import _, lazy_gettext as _l
from models import User

logger = logging.getLogger(__name__)

class LoginForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember me'))
    submit = SubmitField(_l('Sign in'))

class RegisterForm(FlaskForm):
    first_name= StringField(_l('First Name'), validators=[DataRequired(),Length(max=50)])
    last_name= StringField(_l('Last Name'), validators=[DataRequired(),Length(max=100)])
    email = StringField(_l('Email Address'), validators=[Length(min=6, max=50), Email()])
    password = PasswordField(
        _l('Password'), 
        validators=[
            DataRequired(), 
            EqualTo('confirm', message=_l('Passwords must match'))
        ])
    confirm = PasswordField(_l('Repeat Password'), validators=[DataRequired()])
    city= StringField(_l('City'), validators=[DataRequired(),Length(max=100)])
    state= StringField(_l('State'), validators=[DataRequired(),Length(max=100)])
    municipality= StringField(_l('Municipality'), validators=[DataRequired(),Length(max=100)])
    street= StringField(_l('Street'), validators=[DataRequired(),Length(max=300)])
    postal_code= StringField(_l('Postal Code')
                            , validators=[DataRequired(),Length(max=5)])
    exterior_number= StringField(_l('Exterior Number'), validators=[Length(max=10)])
    interior_number= StringField(_l('Interior Number'), 
                                    validators=[DataRequired(),Length(max=10)])
    submit = SubmitField(_l('Register'))

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different email.'))

class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(),Email()])
    submit = SubmitField(_l('Request Password Reset'))

class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired(), Length(max=100)])
    confirm_password = PasswordField(
        _l('Confirm password'), 
        validators = [
            DataRequired(), 
            EqualTo('confirm_password',message=_l('Passwords must match'))
        ])
    submit = SubmitField(_l('Reset Password'))