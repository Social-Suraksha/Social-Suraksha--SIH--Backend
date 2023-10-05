import env
import dataAPI
from dataAPI import data_fetch
import streamlit as st
import pickle
import numpy as np
import warnings
import firebase_admin
from firebase_admin import credentials
warnings.filterwarnings("ignore")
dectree=pickle.load(open('model.pkl','rb'))
cred = credentials.Certificate("creds.json")
firebase_admin.initialize_app(cred,
                              {
                                  'databaseURL': "https://social-suraksha-sih-default-rtdb.asia-southeast1.firebasedatabase.app/"
                              })

from firebase_admin import db

ref = db.reference("/")

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
st.markdown(html_temp, unsafe_allow_html=True)

username = st.text_input(label="Enter the username of the account you want to check", placeholder="Type here")
safe_html="""  
    <div style="background-color:#F4D03F;padding:10px >
    <h2 style="color:white;text-align:center;"> This Account is Real</h2>
    </div>
"""
danger_html="""  
    <div style="background-color:#F08080;padding:10px >
    <h2 style="color:black ;text-align:center;"> This Account is Fake</h2>
    </div>
"""

if st.button("Predict"):
    data = data_fetch(username)
    output=pred(data)
    ref.push({
	username:
	{
		"Real": output,
	}})
    if output:
        st.markdown(safe_html,unsafe_allow_html=True)
    else:
        st.markdown(danger_html,unsafe_allow_html=True)
