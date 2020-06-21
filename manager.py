import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import session
import pyrebase

class Fire():
    def __init__(self):
        self.pyreauth = Fire.init_auth(self)
        self.db = Fire.init_db(self)

    def init_auth(self):
        firebaseConfig = {
            'apiKey': "AIzaSyAopjFhQL0sG7DqIZpxSOf1NyE5pgK5Y7Y",
            'authDomain': "python-practice-c2a44.firebaseapp.com",
            'databaseURL': "https://python-practice-c2a44.firebaseio.com",
            'projectId': "python-practice-c2a44",
            'storageBucket': "python-practice-c2a44.appspot.com",
            'messagingSenderId': "1037362814034",
            'appId': "1:1037362814034:web:ec43adf22c148f0d2a938b"
        }

        pyreApp = pyrebase.initialize_app(firebaseConfig)
        return pyreApp.auth()

    def init_db(self):
        cred = credentials.Certificate("/Users/akshaykumar/Documents/Projects/FlaskLearning/db_example/key.json")
        firebase_admin.initialize_app(cred)
        return firestore.client()

    def create_user(self, email, password):
        self.pyreauth.create_user_with_email_and_password(email, password)
        self.pyreauth.sign_in_with_email_and_password(email, password)

    def login_user(self, email, password):
        self.pyreauth.sign_in_with_email_and_password(email, password)

    def existing_data(self, collection, check, data):
        item = 0
        docs = self.db.collection(collection).where(check, u'==', data).limit(1).stream()
        for doc in docs : item +=1
        return False if item == 0 else True

    def is_user_loggedIn(self, uid):
        if 'uid' in session and uid == session['uid']:
            return True
        return False

    def get_user_info(self, uname):
        doc = self.db.collection(u'users').document(uname).get()
        return doc.to_dict()

    def sign_out_user(self):
        session.pop('uid', None)
        session.pop('username', None)
        session.pop('email', None)
        session.pop('password', None)
        self.pyreauth.current_user = None

    def get_username(self, id):
        return self.db.collection(u'users').document(id).get().to_dict()['uname']



    