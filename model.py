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
  df = pd.read_csv("df.csv", index_col= 0)

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