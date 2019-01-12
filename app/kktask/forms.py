# wt forms
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField , IntegerField , RadioField , TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo , ValidationError
from kktask.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Full Name',
                           validators=[DataRequired(), Length(min=2, max=25)])
    registartion_number = IntegerField('Registration Number',
                           validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    age = IntegerField("Age" , validators=[DataRequired()])
    gender = RadioField('Gender', choices = [('M','Male'),('F','Female')] , validators=[DataRequired()])
    address = TextAreaField("Address" , validators=[DataRequired() , Length(min=10, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_registration_number(self, registration_number):
        user = User.query.filter_by(registration_number=registration_number.data).first()
        if user:
            raise ValidationError('This registration number already exits . Please Log in')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    age = IntegerField("Age" , validators=[DataRequired()])

    address = TextAreaField("Address" , validators=[DataRequired() , Length(min=10, max=150)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')



    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email already exits . Please Log in')

    def validate_age(self, age):
        if age.data != current_user.age:
            user = User.query.filter_by(age=age.data).first()
            if user:
                raise ValidationError('This age already exits')

    def validate_address(self, address):
        if address.data != current_user.address:
            user = User.query.filter_by(address=address.data).first()
            if user:
                raise ValidationError('This address already exits')
