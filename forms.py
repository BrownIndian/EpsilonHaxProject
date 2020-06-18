from flask import Flask,render_template, session, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, IntegerField, SelectField, RadioField
from wtforms.validators import InputRequired, Email, EqualTo, Length, DataRequired

class LoginForm(FlaskForm):
    # email = StringField('Email', validators = [InputRequired()])
    # password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('Email', validators = [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    uname = StringField('Username', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    state = SelectField('State', choices=[('CA', 'California'), ('NY', 'New York'), ('TX', 'Texas')], validators=[DataRequired()])
    zipcode = StringField('Zip', validators=[DataRequired()])
    email = StringField('Email', validators = [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    card_type = SelectField('Card Type', choices=[('v', 'Visa'), ('m', 'MasterCard')], validators=[DataRequired()])
    card_name = StringField('Name on Card', validators=[DataRequired()])
    card_num = StringField('Number on Card', validators=[DataRequired()])
    expiration = StringField('Date', validators=[DataRequired()])
    cvv = StringField('CVV', validators=[DataRequired()])  
    # fname = StringField('First Name', validators=[InputRequired()])
    # lname = StringField('Last Name', validators=[InputRequired()])
    # uname = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    # address = StringField('Address', validators=[InputRequired()])
    # state = SelectField('State', choices=[('CA', 'California'), ('NY', 'New York'), ('TX', 'Texas')], validators=[InputRequired()])
    # zipcode = StringField('Zip', validators=[InputRequired(), Length(min=5, max=5)])
    # email = StringField('Email', validators = [InputRequired(), Email()])
    # password = PasswordField('Password', validators=[InputRequired(), EqualTo('confirmpassword'), Length(min=4, max=15)])
    # confirmpassword = PasswordField('Confirm Password', validators=[InputRequired()])
    # card_type = SelectField('Card Type', choices=[('v', 'Visa'), ('m', 'MasterCard')], validators=[InputRequired()])
    # card_name = StringField('Name on Card', validators=[InputRequired()])
    # card_num = StringField('Number on Card', validators=[InputRequired()])
    # expiration = StringField('Date', validators=[InputRequired()])
    # cvv = StringField('CVV', validators=[InputRequired()])
    # submit = SubmitField('Submit')

   
