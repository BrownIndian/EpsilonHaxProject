from flask import Flask, render_template, session, redirect, request, url_for, flash
from forms import RegisterForm, LoginForm, TaskForm, PreferencesForm, UpdateInfoForm, SignOut
from manager import Fire
import requests

fb = Fire()
auth = fb.pyreauth
db = fb.db
tool = fb.tool

app = Flask(__name__)
app.config['SECRET_KEY'] = "asd2345khkgkjf7saiyd"

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    update_form = UpdateInfoForm()
    preferences_form = PreferencesForm()
    signout = SignOut()
    print(f"This is the current user: {auth.current_user}") 
    user = auth.current_user
    user_info = fb.get_user_info(user['localId'])
    doc_ref = db.collection(u'users').document(user['localId'])

    if update_form.validate_on_submit() and update_form.submit.data:
        doc_ref.update(
        {
        u'address': update_form.address.data,
        u'zipcode': update_form.zipcode.data,
        u'state': update_form.state.data,
        u'card_name': update_form.card_name.data,
        u'card_type': update_form.card_type.data,
        u'card_num': update_form.card_num.data})
        return redirect(url_for("dashboard")) #pls change

    elif preferences_form.validate_on_submit() and preferences_form.submit.data:
        print("Preferences are validated")
        prefs = preferences_form.getPreferences()
        doc_ref.update({u'preferences': prefs})
        return redirect(url_for("profile"))
        
    else:
        for fieldName, errorMessages in update_form.errors.items():
            for err in errorMessages:
                print(err)
    return render_template('profile.html', user_info=user_info, form=update_form, pform = preferences_form, is_logged_in = fb.is_user_loggedIn(), signout_form=signout)

@app.route('/', methods=['GET', 'POST'])
def index():
    signout = SignOut()
    if request.method == "POST":
        fb.sign_out_user()
        return redirect(url_for('index'))
    return render_template('index.html', is_logged_in = fb.is_user_loggedIn(), signout_form=signout)

@app.route('/services', methods=['GET', 'POST'])
def services():
    form = TaskForm()
    signout = SignOut()
    doc_ref = db.collection(u'tasks').stream()

    if form.validate_on_submit():
        session['title'] = form.title.data
        session['description'] = form.description.data
        session['reward'] = form.reward.data
        
        doc_ref = db.collection(u'tasks').document()
        doc_ref.set({
            u'title': form.title.data,
            u'description': form.description.data,
            u'reward': form.reward.data,
         })

        return redirect(url_for('services'))
    return render_template('services.html', form=form, dox = doc_ref, tool=tool, is_logged_in = fb.is_user_loggedIn(), signout_form=signout)

@app.route('/stats')
def stats():
    signout = SignOut()
    return render_template('stats.html', signout_form=signout)

@app.route('/dashboard')
def dashboard():
    signout = SignOut()
    return render_template('dashboard.html', is_logged_in = fb.is_user_loggedIn(), signout_form=signout)


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
                    flash('Thank you for creating an account with us!')

                    doc_ref = db.collection(u'users').document(user['localId'])
                    doc_ref.set({
                    u'fname': form.fname.data,
                    u'lname': form.lname.data,
                    u'uname': form.uname.data,
                    u'email': form.email.data,
                    u'address': form.address.data,
                    u'state': form.state.data,
                    u'card_type': form.card_type.data,
                    u'card_name': form.card_name.data,
                    u'card_num': form.card_num.data,
                    u'expiration': form.expiration.data,
                    u'zipcode': form.zipcode.data,
                    u'cvv': form.cvv.data,
                    u'preferences': ['None']
                    })

                    return redirect(url_for('profile'))
                else:
                    flash('This email already exists within our database')
                    return render_template('register.html', form=form)
        else:   
            return redirect(url_for('index'))
    else:
        if request.method =="POST":
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    flash(err)
            flash('You have made mistakes within the form, please fix them!')
    return render_template('register.html', form=form, is_logged_in = fb.is_user_loggedIn())


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
                flash("You have mispelled your email and/or password")
                return render_template('signin.html', form=form)
            return redirect(url_for('dashboard'))
    return render_template('signin.html', form=form, is_logged_in = fb.is_user_loggedIn())

if __name__ == '__main__':
    app.run(debug=True)
