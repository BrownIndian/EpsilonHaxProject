from flask import Flask, render_template, session, redirect, request, url_for
from forms import RegisterForm, LoginForm
from manager import Fire

app = Flask(__name__)
app.config['SECRET_KEY'] = "asd2345khkgkjf7saiyd"

auth = Fire().init_auth()
db = Fire().init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session['email'] = form.email.data
        session['password'] = form.password.data
        auth.create_user_with_email_and_password(session['email'], session['password'])
        auth.sign_in_with_email_and_password(session['email'], session['password'])

        print(auth.current_user)
        if auth.current_user != None:
            user = auth.current_user
            doc_ref = db.collection(u'users').document(u'pensis')
            doc_ref.set({
                u'fname': form.fname.data,
                u'lname': form.lname.data,
                u'address': form.address.data,
                u'state': form.state.data,
                u'card_t': form.card_type.data,
                u'card_name': form.card_name.data,
                u'card_number': form.card_num.data,
                u'expiration': form.expiration.data,
                u'cvv': form.cvv.data
            })
 
            print("Successfully written to database")

        return redirect(url_for('index'))
    return render_template('register.html', form=form)
    

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        session['email'] = form.email.data
        session['password'] = form.password.data
        if auth.current_user == None:
            user = auth.sign_in_with_email_and_password(session['email'],session['password'])
            return redirect(url_for('index'))
    return render_template('signin.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
    