import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
from lime import lime_tabular

def train_model(gen = False):
  df = pd.read_csv("df.csv", index_col= 0)

  X = df.loc[:, df.columns != "dataset"]
  y = df["dataset"]
  y=y.astype('int')
  fetnames = list(X.columns)

  if gen:
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.3, random_state=42)
    
    ranfor = RandomForestClassifier()
    ranfor = ranfor.fit(X_train, y_train)
    pickle.dump(ranfor,open('model.pkl','wb'))
  explainer_lime = lime_tabular.LimeTabularExplainer(X.values,
                                                   feature_names=fetnames,
                                                   verbose=True,
                                                   mode="classification")
  return explainer_lime