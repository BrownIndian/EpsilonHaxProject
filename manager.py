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

    def service_stats(self, data, role):
        item = 0
        if 'uid' in session:
            docs = self.db.collection(u'tasks').where(role, u'==', data).stream()
        for doc in docs : item +=1
        return item


class Picture():
    def __init__(self):
        self.picture = {
            'Errands': 'https://img1.wsimg.com/isteam/ip/19b4fe79-5637-4b7c-973d-a9a082153f0e/10ad03f1-03bd-4fa5-b2dc-3adcaf8b47a2.jpeg/:/cr=t:0%25,l:0%25,w:100%25,h:100%25/rs=h:1000,cg:true',
            'Delivery': 'https://cdn-b.william-reed.com/var/wrbm_gb_hospitality/storage/images/publications/hospitality/bighospitality.co.uk/article/2020/01/28/the-future-of-restaurant-delivery/3268223-2-eng-GB/The-future-of-restaurant-delivery_wrbm_large.jpg',
            'Help Moving': 'https://i2.wp.com/movingtips.wpengine.com/wp-content/uploads/2019/02/moving-boxes-crosscountry.jpg?fit=1024%2C684&ssl=1',
            'Tutoring': 'https://images.theconversation.com/files/268439/original/file-20190409-2921-1a4uike.jpg?ixlib=rb-1.1.0&q=45&auto=format&w=1000&fit=clip',
            'Plumbing': 'https://wateroutfortwayne.com/wp-content/uploads/2019/09/shutterstock_1149190532.jpg',
            'Cleaning': 'https://2rdnmg1qbg403gumla1v9i2h-wpengine.netdna-ssl.com/wp-content/uploads/sites/3/2018/11/cleanSick-628306310_770x533-650x428.jpg',
            'Repairs': 'https://article.images.consumerreports.org/f_auto/prod/content/dam/CRO%20Images%202018/Electronics/March/CR-Electronics-InlineHero-right-to-repair-0318',
            'Gardening': 'https://images.everydayhealth.com/images/lung-respiratory/allergies/cs-yard-work-tips-when-you-have-allergies-1440x810.jpg?sfvrsn=45092c15_0',
        }