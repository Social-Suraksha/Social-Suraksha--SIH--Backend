import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score,precision_score,recall_score, log_loss
import pickle
def train_model():
  df = pd.read_csv("fusers.csv")
  df1 = pd.read_csv("users.csv")
  df = pd.concat([df1,df], axis=0)
  df.reset_index(drop=True, inplace=True)
  df = df.loc[:, df.columns != "created_at"]
  df = df.loc[:, df.columns != "profile_background_image_url"]
  df = df.loc[:, df.columns != "lang"]
  df = df.loc[:, df.columns != "url"]
  df = df.loc[:, df.columns != "profile_text_color"]
  df = df.loc[:, df.columns != "profile_background_image_url_https"]
  df = df.loc[:, df.columns != "profile_banner_url"]
  df = df.loc[:, df.columns != "id"]
  df = df.loc[:, df.columns != "protected"]
  df = df.loc[:, df.columns != "verified"]
  df = df.loc[:, df.columns != "profile_image_url_https"]
  df.loc[df['dataset'] == "E13", 'dataset'] = 1
  df.loc[df['dataset'] == "TFP", 'dataset'] = 1
  df.loc[df['dataset'] == "INT", 'dataset'] = 0
  df.loc[df['dataset'] == "TWT", 'dataset'] = 0
  df.loc[df['dataset'] == "FSF", 'dataset'] = 0
  df['description'].fillna(0, inplace=True)
  df.loc[df['description'] != 0, 'description'] = 1
  df.loc[df['default_profile'] != 1, 'default_profile'] = 0
  df = df.loc[:, df.columns != "time_zone"]
  df = df.loc[:, df.columns != "location"]
  df = df.loc[:, df.columns != "profile_use_background_image"]
  df = df.loc[:, df.columns != "default_profile_image"]
  df = df.loc[:, df.columns != "profile_image_url"]
  df = df.loc[:, df.columns != "geo_enabled"]
  df = df.loc[:, df.columns != "fav_number"]
  df.loc[df['profile_background_tile'] != 1, 'profile_background_tile'] = 0
  df = df.loc[:, df.columns != "updated"]
  df.loc[df['profile_sidebar_border_color'] != "C0DEED", 'profile_sidebar_border_color'] = 0
  df.loc[df['profile_sidebar_border_color'] == "C0DEED", 'profile_sidebar_border_color'] = 1
  df.loc[df['profile_sidebar_fill_color'] != "DDEEF6", 'profile_sidebar_fill_color'] = 0
  df.loc[df['profile_sidebar_fill_color'] == "DDEEF6", 'profile_sidebar_fill_color'] = 1
  df = df.loc[:, df.columns != "profile_link_color"]
  df = df.loc[:, df.columns != "profile_background_color"]
  df = df.loc[:, df.columns != "utc_offset"]
  df

  df = df.loc[:, df.columns != "name"]
  df = df.loc[:, df.columns != "screen_name"]
  df

  X = df.loc[:, df.columns != "dataset"]
  y = df["dataset"]
  y=y.astype('int')
  df.isnull().values.any()

  X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.3, random_state=42)


  dectree = DecisionTreeClassifier()
  dectree = dectree.fit(X_train,y_train)

  pickle.dump(dectree,open('model.pkl','wb'))

