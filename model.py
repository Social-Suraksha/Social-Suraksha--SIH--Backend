import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import plot_tree
import pickle
import matplotlib.pyplot as plt
from lime import lime_tabular

def train_model(gen = False):
  df = pd.read_csv("fusers.csv")
  df1 = pd.read_csv("users.csv")
  df = pd.concat([df1,df], axis=0)
  df.reset_index(drop=True, inplace=True)
  columns_to_drop = [
      "created_at",
      "profile_background_image_url",
      "lang",
      "url",
      "profile_text_color",
      "profile_background_image_url_https",
      "profile_banner_url",
      "id",
      "protected",
      "verified",
      "profile_image_url_https",
      "time_zone",
      "location",
      "profile_use_background_image",
      "default_profile_image",
      "profile_image_url",
      "geo_enabled",
      "fav_number",
      "profile_link_color",
      "profile_background_color",
      "utc_offset",
      "updated",
      "name",
      "screen_name",
  ]

  df = df.drop(columns = columns_to_drop)
  mapping = {'E13': 1, 'TFP': 1, 'INT': 0, 'TWT': 0, 'FSF': 0}
  df['dataset'] = df['dataset'].replace(mapping)
  df['description'].fillna(0, inplace = True)
  df['default_profile'].fillna(0, inplace = True) 
  df["profile_background_tile"].fillna(0, inplace = True)
  df['profile_sidebar_border_color'] = np.where(df['profile_sidebar_border_color'] == "C0DEED", 1, 0)
  df['profile_sidebar_fill_color'] = np.where(df['profile_sidebar_fill_color'] == "DDEEF6", 1, 0)
  df['description'] = np.where(df['description'] != 0, 1, 0)

  X = df.loc[:, df.columns != "dataset"]
  y = df["dataset"]
  y=y.astype('int')

  X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.3, random_state=42)
  fetnames = list(X.columns)
  
  ranfor = RandomForestClassifier()
  ranfor = ranfor.fit(X_train, y_train)
  
  # if plot and model:
  #   for tree_idx, estimator in enumerate(ranfor.estimators_):
  #     plt.figure(figsize=(20, 11.25))
  #     plot_tree(estimator, filled=True, feature_names=X.columns)
  #     plt.title(f'Decision Tree {tree_idx}')
  #     plt.savefig(f"visualisations/tree_{tree_idx}.pdf", dpi = 2400)
  #     print(tree_idx)
  #     plt.close()
  # elif plot or model:
  #     plt.figure(figsize=(20, 11.25))
  #     plot_tree(dectree, filled=True, feature_names=X.columns)
  #     plt.title(f'Decision Tree')
  #     plt.savefig(f"visualisations/dectree.pdf", dpi = 2400)
  #     plt.close()
  if gen:
    pickle.dump(ranfor,open('model.pkl','wb'))
  explainer_lime = lime_tabular.LimeTabularExplainer(X.values,
                                                   feature_names=fetnames,
                                                   verbose=True,
                                                   mode="classification")
  return explainer_lime