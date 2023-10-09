import dataAPI
from dataAPI import data_fetch
import streamlit as st
import pickle
import numpy as np
import warnings
import firebase_admin
import firebase
from firebase_admin import db
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
    ref = db.reference("/")
    stored_rec = ref.get()
    if stored_rec != None:
        if username not in stored_rec.keys():
            data = data_fetch(username)
            output=pred(data)
            ref = db.reference(f"/{username}")
            if output == True :ref.set("Real")
            else : ref.set("Fake")
        else:
            output = stored_rec[username]
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
