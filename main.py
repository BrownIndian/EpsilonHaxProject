from flask import Flask, render_template, session, redirect, request, url_for, flash
from forms import RegisterForm, LoginForm
from manager import Fire
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = "asd2345khkgkjf7saiyd"

fb = Fire()
auth = fb.pyreauth
db = fb.db


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session['email'] = form.email.data
        session['password'] = form.password.data
        session['uname'] = form.uname.data

        if auth.current_user == None: 
            if fb.existing_data(u'uname', form.uname.data):
                print("Username is already taken") # Send to user
                return redirect(url_for('register'))
            else:
                if fb.existing_data(u'email', form.email.data):
                    fb.create_user(session['email'],session['password'])
                else:
                    return redirect(url_for('register'))
                    
                user = auth.current_user
                user['displayName'] = form.uname.data

                doc_ref = db.collection(u'users').document(user['displayName'])
                doc_ref.set({
                u'fname': form.fname.data,
                u'lname': form.lname.data,
                u'uname': form.uname.data,
                u'address': form.address.data,
                u'state': form.state.data,
                u'card_t': form.card_type.data,
                u'card_name': form.card_name.data,
                u'card_number': form.card_num.data,
                u'expiration': form.expiration.data,
                u'cvv': form.cvv.data,
            })

        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        session['email'] = form.email.data
        session['password'] = form.password.data
        if auth.current_user == None:
            try:
                fb.login_user(session['email'],session['password'])
            except requests.exceptions.HTTPError:
                print("You have mispelled your email and/or password") #Send to user
            finally:
                return redirect(url_for('signin'))
            return redirect(url_for('index'))
    return render_template('signin.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
