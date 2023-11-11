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
import model
from lime import lime_tabular
warnings.filterwarnings("ignore")
try:
    ranfor=pickle.load(open('model.pkl','rb'))
except FileNotFoundError:
    explainer_lime = model.train_model(gen=True)
    ranfor=pickle.load(open('model.pkl','rb'))

st.set_page_config(page_title="Fake Account Checker", page_icon="👨‍💻")

def explain(explainer_lime, input_data):
    exp_lime = explainer_lime.explain_instance(
    np.array(input_data), ranfor.predict_proba, num_features=9)
    st.components.v1.html(exp_lime.as_html())
    st.pyplot(exp_lime.as_pyplot_figure())

def pred(features):
    input_data = input_data = np.column_stack(features)
    result = ranfor.predict(input_data)
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
st.markdown("We are facing a technical issue causing profiles to be incorrectly identified as suspended due to changes to the Twitter API, and are working on a solution, please standby.")
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
    if "https://twitter.com/" in username:
        username = username[20:]
    elif"twitter.com/" in username:
        username = username[12:]
    username = username.lower()
    ref = db.reference("/")
    stored_rec = ref.get()
    try:
        data = data_fetch(username)
    except tweepy.NotFound:
        st.markdown("The account you are looking for does not exist, please check the Username entered.")
        st.stop()
    except tweepy.Forbidden as e:
        st.markdown("The account you are looking for has been suspended for violating [X Rules](https://support.twitter.com/articles/18311), please check the Username entered.")
        # ref = db.reference(f"/{username}")
        # ref.set("Suspended")
        output = "Suspended"
        st.stop()
    except tweepy.Unauthorized:
        st.markdown("We are facing a technical issue, please try again later or submit an issue on the GitHub page")
        st.stop()
    output=pred(data)
    ref = db.reference(f"/{username}")
    if output == True :ref.set("Real")
    else : ref.set("Fake")
    if output:
        st.markdown(safe_html,unsafe_allow_html=True)
        explain(model.train_model(), data)
    elif output == "Suspended":
        st.markdown("The account you are looking for has been suspended for violating [X Rules](https://support.twitter.com/articles/18311), please check the Username entered.")
    else:
        st.markdown(danger_html,unsafe_allow_html=True)
        explain(model.train_model(), data)