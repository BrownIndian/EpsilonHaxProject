from flask import Flask,render_template, session, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, IntegerField, SelectField, RadioField, BooleanField, TextField
from wtforms.validators import InputRequired, Email, EqualTo, Length, Optional
from wtforms.widgets import TextArea

#TRY TO IMPLEMENT MESSAGES ERROR SYSTEM
class LoginForm(FlaskForm):
    email = StringField('Email', validators = [InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    fname = StringField('First Name', validators=[InputRequired(message="Type in your name please")])
    lname = StringField('Last Name', validators=[InputRequired(message="Type in your last name please")])
    uname = StringField('Username', validators=[InputRequired(message="Invalid Username: Between 1 to 15 characters"), Length(min=1, max=15)])
    address = StringField('Address', validators=[InputRequired(message="Type in your address please")])
    state = SelectField('State', choices=[('CA', 'California'), ('NY', 'New York'), ('TX', 'Texas')], validators=[InputRequired()])
    zipcode = StringField('Zip', validators=[InputRequired(message="Invalid Zipcode"), Length(min=5, max=5)])
    email = StringField('Email', validators = [InputRequired(), Email(message="Invalid Email Address")])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('confirmpassword', message="Confirm Password does not match the password field"), Length(min=4, max=15)])
    confirmpassword = PasswordField('Confirm Password', validators=[InputRequired()])
    card_type = SelectField('Card Type', choices=[('Visa', 'Visa'), ('MasterCard', 'MasterCard')], validators=[InputRequired()])
    card_name = StringField('Name on Card', validators=[InputRequired(message="Type the name on your credit card please")])
    card_num = StringField('Number on Card', validators=[InputRequired(message="Type the number on your card please")])
    expiration = StringField('Date', validators=[InputRequired(message="Type the expiration date")])
    cvv = StringField('CVV', validators=[InputRequired(message="Invalid CVV")])
    submit = SubmitField('Submit')

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    address = StringField('Address', validators=[InputRequired()])
    state = SelectField('State', choices=[(None, 'State'),('CA', 'California'), ('NY', 'New York'), ('TX', 'Texas'), ('FL', 'Florida'), ('WA', 'Washington'), ('VA', 'Virginia'), ('GA', 'Georgia')], validators=[InputRequired()])
    category = SelectField('Category', choices=[(None, 'Category'),('Errands', 'Errands'), ('Delivery', 'Delivery'), ('Help Moving', 'Help Moving'), ('Tutoring', 'Tutoring'), ('Plumbing', 'Plumbing'), ('Cleaning', 'Cleaning'), ('Repairs', 'Repairs'), ('Gardening', 'Gardening')], validators=[InputRequired()])
    city = StringField('City', validators=[InputRequired()])
    zipcode = StringField('Zipcode', validators=[InputRequired()])
    description = StringField('Description', widget=TextArea(), validators=[InputRequired()])
    reward = StringField('Reward', validators=[InputRequired()])
    submit = SubmitField('Submit')

class UpdateInfoForm(FlaskForm):
    address = StringField('Address', validators=[Optional()])
    state = SelectField('State', choices=[('CA', 'California'), ('NY', 'New York'), ('TX', 'Texas')], validators=[Optional()])
    zipcode = StringField('Zip', validators=[InputRequired(), Length(min=5, max=5)])
    password = PasswordField('Password', validators=[Optional(), EqualTo('confirmpassword'), Length(min=4, max=15)])
    confirmpassword = PasswordField('Confirm Password', validators=[Optional()])
    card_type = SelectField('Card Type', choices=[('Visa', 'Visa'), ('MasterCard', 'MasterCard')], validators=[Optional()])
    card_name = StringField('Name on Card', validators=[Optional()])
    card_num = StringField('Number on Card', validators=[Optional()])
    expiration = StringField('Date', validators=[Optional()])
    cvv = StringField('CVV', validators=[Optional()])
    submit = SubmitField('Submit')

class PreferencesForm(FlaskForm):
    tech = BooleanField("Technology", description="Technology")
    gardening = BooleanField("Gardening", description="Gardening")
    cleaning = BooleanField("Cleaning", description="Cleaning")
    submit = SubmitField('Submit')

    def ptype(self):
        return (self.tech, self.gardening, self.cleaning)

    def getPreferences(self):
        prefs = []
        for pref in self.ptype():
            if pref.data:
                prefs.append(pref.description)
        return ['None'] if len(prefs) == 0 else prefs

class SearchForm(FlaskForm):
    search = TextField('Search', validators=[Optional()])
    state = SelectField('State', choices=[(None, 'Choices'),('CA', 'California'), ('NY', 'New York'), ('TX', 'Texas'), ('FL', 'Florida'), ('WA', 'Washington'), ('VA', 'Virginia'), ('GA', 'Georgia')], validators=[InputRequired()])
    category = SelectField('Category', choices=[(None, 'Choices'), ('Errands', 'Errands'), ('Delivery', 'Delivery'), ('Help Moving', 'Help Moving'), ('Tutoring', 'Tutoring'), ('Plumbing', 'Plumbing'), ('Cleaning', 'Cleaning'), ('Repairs', 'Repairs'), ('Gardening', 'Gardening')], validators=[Optional()])
    submit = SubmitField('Search')

class SignOut(FlaskForm):
    submit = SubmitField('Sign Out')

class AcceptService(FlaskForm):
    submit = SubmitField('Accept Job')

class MarkDone(FlaskForm):
    submit = SubmitField('Mark as Done', render_kw={'style': "float: right;"}, id="mark")

class ConfirmDone(FlaskForm):
    submit = SubmitField('Confirm as Done', render_kw={'style': "float: right;"}, id="confirm")
