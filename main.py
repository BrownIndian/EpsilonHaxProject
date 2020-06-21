from flask import Flask, render_template, session, redirect, request, url_for, flash
from forms import RegisterForm, LoginForm, TaskForm, PreferencesForm, UpdateInfoForm, SignOut, AcceptService, MarkDone, ConfirmDone
from manager import Fire
import requests, uuid, datetime, time

fb = Fire()
auth = fb.pyreauth
db = fb.db

app = Flask(__name__)
app.config['SECRET_KEY'] = "asd2345khkgkjf7saiyd"

@app.route('/', methods=['GET', 'POST'])
def index():
    signout = SignOut()
    if request.method == "POST":
        fb.sign_out_user()
        return redirect(url_for('index'))
    return render_template('index.html', signout_form=signout)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session['email'] = form.email.data
        session['password'] = form.password.data
        session['uname'] = form.uname.data

        if 'uid' not in session: 
            print(fb.existing_data(u'user',u'uname', form.uname.data))
            if fb.existing_data(u'user',u'uname', form.uname.data):
                print(form.uname.data)
                flash("Username is already taken") # Send to user
                form.uname.data = ''
                return render_template('register.html', form=form)
            else:
                if not fb.existing_data(u'user',u'email', form.email.data):
                    fb.create_user(session['email'],session['password'])
                    session['uid'] = auth.current_user['localId']
                    flash('Thank you for creating an account with us!')

                    doc_ref = db.collection(u'users').document(session['uid'])
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
                    u'money': 0,
                    u'datejoined': datetime.datetime.now().strftime("%x"),
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
    return render_template('register.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        session['email'] = form.email.data
        session['password'] = form.password.data

        if 'uid' not in session:
            try:
                fb.login_user(session['email'],session['password'])
                session['uid'] = auth.current_user['localId']
                session['uname'] = fb.get_username(session['uid'])

            except requests.exceptions.HTTPError:
                flash("You have mispelled your email and/or password")
                return render_template('signin.html', form=form)
            return redirect(url_for('dashboard'))
    return render_template('signin.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    signout = SignOut()
    mark = MarkDone()
    confirm = ConfirmDone()
    user = fb.get_username(session['uid'])

    if confirm.validate_on_submit() or mark.validate_on_submit():
        if 'markasdone' in request.form:
            marked = bool(request.form['markasdone'])
            doc_ref = db.collection(u'tasks').document(request.form['mdoc_id'])
            doc_ref.update({u'wfinished': marked})
            return redirect(url_for('dashboard'))
        elif 'confirmdone' in request.form:
            confirmed = bool(request.form['confirmdone'])
            doc_ref = db.collection(u'tasks').document(request.form['doc_id'])
            doc_ref.update({u'finished': confirmed})

            service = doc_ref.get().to_dict()
            worker_uname = service['worker']
            workers = db.collection(u'users').where(u'uname', u'==', worker_uname).limit(1).stream()
            worker_id = ''
            for worker in workers:
                worker_id = worker.id

            worker_ref = db.collection(u'users').document(worker_id)
            money = worker_ref.get().to_dict()['money']
            money+=int(service['reward'])
            worker_ref.update({u'money': money})
            
            return redirect(url_for('dashboard'))

    services_offered = db.collection(u'tasks').where(u'worker', u'==', user).limit(5).stream()
    services_requested = db.collection(u'tasks').where(u'creator', u'==', user).limit(5).stream()
    services_completed = db.collection(u'tasks').where(u'finished', u'==', True).limit(5).stream()

    offered_exists = fb.existing_data(u'tasks', u'worker', user)
    requested_exists = fb.existing_data(u'tasks', u'creator', user)
    completed_exists = fb.existing_data(u'tasks', u'finished', True)
    
    return render_template('dashboard.html', signout_form=signout, offered = services_offered, requested = services_requested, completed = services_completed, o_e = offered_exists, r_e = requested_exists, c_e = completed_exists, mark=mark, confirm=confirm)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    update_form = UpdateInfoForm()
    preferences_form = PreferencesForm()
    signout = SignOut()

    user_info = fb.get_user_info(session['uid'])
    doc_ref = db.collection(u'users').document(session['uid'])

    services_requested = fb.service_stats(session['uname'], u'creator')
    services_done = fb.service_stats(session['uname'], u'creator')

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
    return render_template('profile.html', user_info=user_info, form=update_form, pform = preferences_form, signout_form=signout, sr = services_requested, sd = services_done)

@app.route('/services', methods=['GET', 'POST'])
def services():
    form = TaskForm()
    acc_ser = AcceptService()
    signout = SignOut()
    doc_ref = db.collection(u'tasks').where(u'accepted', u'==', False).stream()


    if form.validate_on_submit():
        doc_ref = db.collection(u'tasks').document()
        doc_ref.set({
            u'creator': session['uname'],
            u'worker': '',
            u'finished': False,
            u'dateCreated': datetime.datetime.now(),
            u'dateFinished': '',
            u'title': form.title.data,
            u'description': form.description.data,
            u'reward': form.reward.data,
            u'accepted': False,
            u'wfinished': False
        })
        return redirect(url_for('services'))

    elif acc_ser.validate_on_submit():
        
        if acc_ser.submit.data:
            service_id = request.form['index']
            doc_ref = db.collection(u'tasks').document(service_id)
            
            if doc_ref.get().exists:
                if not doc_ref.get().to_dict()['creator'] == session['uname']:
                    doc_ref.update({
                        u'worker': session['uname'],
                        u'dateAccepted': datetime.datetime.now(),
                        u'accepted':True
                    })
                    return redirect('services')
                else:
                    flash("You cannot do tasks that you have created")
                    
            return redirect('services')
    else:
        for fieldName, errorMessages in acc_ser.errors.items():
            for err in errorMessages:
                print(err)
    return render_template('services.html', form=form, dox = doc_ref, signout_form=signout, acc_ser=acc_ser)


if __name__ == '__main__':
    app.run(debug=True)


