import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import os

import numpy as np
import pandas as pd
import tensorflow as tf

import atecml.data

from contextlib import contextmanager
from tqdm import tqdm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from imblearn.over_sampling import SMOTE, ADASYN
from sklearn.externals import joblib


def predict_proba_matrix(trained_model_list, df):
    low_band = 0.05
    high_band = 0.5
    data = df.reset_index(drop=True)
    verify_df = pd.DataFrame()
    extend_feature = []
    with atecml.data.timer("Validation....."):
        for idx in tqdm(range(len(trained_model_list))):
            clf = trained_model_list[idx]
            model_params = train_model[idx].split("__")
            f_idx = int(model_params[3])
            select_feature = feature_list[f_idx]
            y_predict = clf.predict(data[select_feature])
            if model_params[1] == "Fraud":
                verify_df["n" + str(idx)] = abs(y_predict)
            else:
                verify_df["n" + str(idx)] = abs(1 - y_predict)
            ext = pd.DataFrame(clf.apply(data[select_feature])).T
            extend_feature.append(ext)

    v_var = verify_df.var(axis=1)
    v_mean = verify_df.mean(axis=1)
    v_skew = verify_df.skew(axis=1)
    v_kurt = verify_df.T.kurt(axis=1)
    verify_df["var"] = v_var
    verify_df["mean"] = v_mean
    verify_df["skew"] = v_skew
    verify_df["kurt"] = v_kurt

    ext_df = pd.concat(extend_feature, ignore_index=True)
    # ext_df = pd.concat([ext_df_tmp.T,data['id']],axis=1)

    result = pd.concat([verify_df, data["id"]], axis=1)
    filter_id_list = list(
        result[(result["mean"] > low_band) & (result["mean"] < high_band)]["id"]
    )
    residual_df = data[data["id"].isin(filter_id_list)].reset_index(drop=True)

    return result, residual_df, ext_df


# Loading Data....
data = atecml.data.load_train()
train_df = atecml.data.filter_date(data, start_date="2017-09-05", end_date="2017-10-15")
val_df = atecml.data.filter_date(data, start_date="2017-10-16", end_date="2018-10-15")

predictors = [x for x in train_df.columns if x not in atecml.data.NOT_FEATURE_SUM]

# Loading Data....
data = atecml.data.load_train()
predictors = [x for x in data.columns if x not in atecml.data.NOT_FEATURE_SUM]


feature_tree_num = 10
train_model = []
target_list = ["Normal", "Fraud"]
# target_list = ['Normal']
# target_list = ['Fraud']

for idx in range(0, 1):
    for item in ["dart", "gbdt", "rf"]:
        for feature_grp_idx in range(0, feature_tree_num):
            for target in target_list:
                train_id = (
                    item + "__" + target + "__" + str(idx) + "__" + str(feature_grp_idx)
                )
                train_model.append(train_id)


def model_load(model_name):
    model_cache_name = "./" + model_name + ".model"
    if os.path.exists(model_cache_name):
        clf = joblib.load(model_cache_name)
    else:
        print("ERROR...............")
    return clf


if os.path.exists("./feature_list.dat"):
    print("Load Feature List from persistant store...")
    feature_list = joblib.load("./feature_list.dat")
else:
    print("Error: Feature Cache File missing...")


trained_model_list = []
with atecml.data.timer("Classification: Model Training"):
    for train_id in tqdm(range(len(train_model))):
        fit_model = model_load(train_model[train_id])
        trained_model_list.append(fit_model)

result, res, ext = predict_proba_matrix(trained_model_list, data)

result.to_pickle("./result.df")
res.to_pickle("./res.df")
ext.to_pickle("./ext.df")
