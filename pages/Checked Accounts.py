import streamlit as st
import firebase_admin
import firebase
from firebase_admin import db
import pandas as pd
st.set_page_config(page_title="Checked Accounts Database", page_icon="ℹ")

st.title("Checked Accounts List")
html_temp = """
<div style="background-color:#025246 ;padding:10px">
<h2 style="color:white;text-align:center;">The following accounts have been checked using our Website: </h2>
</div>
"""
st.markdown(html_temp, unsafe_allow_html=True)

ref = db.reference("/")
stored_rec = ref.get()
try:
    df = pd.DataFrame.from_dict(stored_rec,orient="index", columns=["Fake/Real"])
    st.dataframe(df, use_container_width=True)
except ValueError:
    st.markdown("No accounts have been checked yet.")


