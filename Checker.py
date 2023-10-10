import dataAPI
from dataAPI import data_fetch
import streamlit as st
import pickle
import numpy as np
import warnings
import firebase_admin
import firebase
from firebase_admin import db
import tweepy
warnings.filterwarnings("ignore")
dectree=pickle.load(open('model.pkl','rb'))

st.set_page_config(page_title="Fake Account Checker", page_icon="👨‍💻")

def pred(features):
    input_data = input_data = np.column_stack(features)
    result = dectree.predict(input_data)
    if 1 in result:
        return True
    else:
        return False
    
st.title("Fake Account Checker")
html_temp = """
<div style="background-color:#025246 ;padding:10px">
<h2 style="color:white;text-align:center;">Check for Fake Twitter Accounts </h2>
</div>
"""
safe_html="""  
    <div style="background-color:#00FF00;padding:10px >
    <h2 style="color:white; text-align:center;"><span style="color: black;"> <b>This Account is Real</b></span></h2>
    </div>
"""
danger_html="""  
    <div style="background-color:#FF0000;padding:10px >
    <h2 style="color:white ; text-align:center;"><span style="color: black;"> <b>This Account is Fake</b></span></h2>
    </div>
"""
st.markdown(html_temp, unsafe_allow_html=True)

username = st.text_input(label="Enter the username of the account you want to check", placeholder="Type here")

if st.button("Predict"):
    if username[0] == "@":
        username = username[1:]
    ref = db.reference("/")
    stored_rec = ref.get()
    if stored_rec != None:
        if username not in stored_rec.keys():
            try:
                data = data_fetch(username)
            except tweepy.NotFound:
                st.markdown("The account you are looking for does not exist, please check the Username entered.")
                st.stop()
            output=pred(data)
            ref = db.reference(f"/{username}")
            if output == True :ref.set("Real")
            else : ref.set("Fake")
        else:
            if stored_rec[username] == "Fake" : output = False
            else : output = True
    else:
        data = data_fetch(username)
        output=pred(data)
        ref = db.reference(f"/{username}")
        if output == True :ref.set("Real")
        else : ref.set("Fake")
    if output:
        st.markdown(safe_html,unsafe_allow_html=True)
    else:
        st.markdown(danger_html,unsafe_allow_html=True)
