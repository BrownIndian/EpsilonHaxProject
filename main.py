from flask import Flask, render_template, session, redirect, request, url_for, flash
from forms import RegisterForm, LoginForm
from manager import Fire
import requests

fb = Fire()
auth = fb.pyreauth
db = fb.db

app = Flask(__name__)
app.config['SECRET_KEY'] = "asd2345khkgkjf7saiyd"



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
            print(fb.existing_data(u'uname', form.uname.data))
            if fb.existing_data(u'uname', form.uname.data):
                print(form.uname.data)
                flash("Username is already taken") # Send to user
                form.uname.data = ''
                return render_template('register.html', form=form)
            else:
                if not fb.existing_data(u'email', form.email.data):
                    print(form.email.data)
                    fb.create_user(session['email'],session['password'])
                    user = auth.current_user
                    user['displayName'] = form.uname.data
                    flash('Thank you for creating an account with us!')

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
                    u'cvv': form.cvv.data })

                    return redirect(url_for('index'))
                else:
                    flash('This email already exists within our database')
                    return render_template('register.html', form=form)
        else:   
            return redirect(url_for('index'))
    else:
        if request.method =="POST":
            flash('You have made mistakes within the form, please fix them!')
    return render_template('register.html', form=form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        session['email'] = form.email.data
        session['password'] = form.password.data

        print(f"{auth.current_user} sfhasflkfhsa klhsdkffkdsjk skfdhkfh hjd f" )
        if auth.current_user == None:
            try:
                fb.login_user(session['email'],session['password'])
            except requests.exceptions.HTTPError:
                flash("You have mispelled your email and/or password")

            return redirect(url_for('index'))
    return render_template('signin.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
