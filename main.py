from flask import Flask, render_template, session, redirect, request, url_for, flash
from forms import RegisterForm, LoginForm
'''
from manager import Fire
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = "asd2345khkgkjf7saiyd"
'''
auth = Fire().init_auth()
db = Fire().init_db()
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session['email'] = form.email.data
        session['password'] = form.password.data
        return redirect(url_for('index'))
        '''
        auth.create_user_with_email_and_password(session['email'], session['password'])
        auth.sign_in_with_email_and_password(session['email'], session['password'])
        '''
    else:
        flash('One or more of your fields is not invalid. Please follow the field instructions and submit again.')

    return render_template('register.html', form=form)



@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        session['email'] = form.email.data
        session['password'] = form.password.data

        return redirect(url_for('index'))
    return render_template('signin.html', form=form)
''' (move to above return redirect)
if auth.current_user == None:
    user = auth.sign_in_with_email_and_password(session['email'],session['password'])
    '''

if __name__ == '__main__':
    app.run(debug=True)
