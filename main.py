from flask import Flask, render_template, session
from forms import RegisterForm, LoginForm
from manager import Fire

app = Flask(__name__)
app.config['SECRET_KEY'] = "asd2345khkgkjf7saiyd"

@app.route('/', methods=['GET, POST'])
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        pass
    return render_template('register.html', form=form)
    
@app.route('/signin')
def signin():
    return render_template('signin.html')


if __name__ == '__main__':
    app.run(debug=True)