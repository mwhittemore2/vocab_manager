from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models import User

class LoginForm(FlaskForm):
    email_validators = [DataRequired(), Length(1,64), Email()]
    email = StringField('Email', validators=email_validators)

    password_validators = [DataRequired()]
    password = PasswordField('Password', validators=password_validators)

    stay_logged_in = BooleanField("Stay logged in")

    submit = SubmitField("Log In")

class RegistrationForm(FlaskForm):
    email_validators=[DataRequired(), Length(1,64), Email()]
    email = StringField('Email', validators=email_validators)

    first_name_validators = [DataRequired(), Length(1,64)]
    first_name_regex_string = '^[A-Za-z]+$'
    first_name_regex_error = 'First name must contain only letters'
    first_name_regexp_validator = Regexp(first_name_regex_string, 0, first_name_regex_error)
    first_name_validators.append(first_name_regexp_validator)
    first_name = StringField('First name', validators=first_name_validators)

    last_name_validators = [DataRequired(), Length(1,64)]
    last_name_regex_string = '^[A-Za-z]+$'
    last_name_regex_error = 'Last name must contain only letters'
    last_name_regex_validator = Regexp(last_name_regex_string, 0, last_name_regex_error)
    last_name_validators.append(last_name_regex_validator)
    last_name = StringField('Last name', validators=last_name_validators)

    password_validators = [DataRequired()]
    equal_to = EqualTo('password2', message='Passwords must match')
    password_validators.append(equal_to)
    password = PasswordField('Password', validators=password_validators)
    password2 = PasswordField('Confirm password', validators=[DataRequired()])

    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.objects(email=field.data).first():
            raise ValidationError("Email already registered")