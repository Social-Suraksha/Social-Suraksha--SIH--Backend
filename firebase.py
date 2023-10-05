import firebase_admin
from firebase_admin import credentials
if not firebase_admin._apps:
    cred = credentials.Certificate("creds.json")
    firebase_admin.initialize_app(cred,
                              {
                                  'databaseURL': "https://social-suraksha-sih-default-rtdb.asia-southeast1.firebasedatabase.app/"
                              })