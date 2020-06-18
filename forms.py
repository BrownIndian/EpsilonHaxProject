from flask import Flask,render_template, session, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, IntegerField, SelectField, RadioField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    uname = StringField('Username', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    state = SelectField('State', choices=[('CA', 'California'), ('NY', 'New York'), ('TX', 'Texas')], validators=[DataRequired()])
    zipcode = IntegerField('Zip', validators=[DataRequired()])
    email = StringField('Email', validators = [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    card_type = SelectField('Card Type', choices=[('v', 'Visa'), ('m', 'MasterCard')], validators=[DataRequired()])
    card_name = StringField('Name on Card', validators=[DataRequired()])
    card_num = IntegerField('Number on Card', validators=[DataRequired()])
    expiration = DateField('Date', validators=[DataRequired()])
    cvv = IntegerField('CVV', validators=[DataRequired()])    
    submit = SubmitField('Submit')
