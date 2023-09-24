import env
import dataAPI
import streamlit as st
import pickle
import numpy as np
import warnings
warnings.filterwarnings("ignore")
dectree=pickle.load(open('model.pkl','rb'))

def pred(features):
    input_data = input_data = np.column_stack(features)
    result = dectree.predict(input_data)
    if 1 in result:
        return True
    else:
        return False
    
print(pred(dataAPI.data_fetch("al3649")))
