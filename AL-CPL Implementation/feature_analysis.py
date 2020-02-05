import pandas as pd
import numpy as np

import sklearn
from sklearn.preprocessing import scale

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC

from sklearn.model_selection import train_test_split, KFold
from sklearn import metrics
from sklearn import preprocessing
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, roc_auc_score


# Data Reading
file_names = ["output/data_mining.csv",
              "output/geometry.csv",
              "output/physics.csv",
              "output/precalculus.csv"]

methods =  ["RF"]

feature_index = ["outd A", "outd B", "ind A", "ind B", "#cat A", "#cat B", "common neighbors",
                "common categories", "# A links to B", "# B links to A", "RefD", "A in B's first sent",
                "B in A's first sent", "B in A's title", "NGD", "|In_A\cap In_B|/|In_A|",
                "|In_A\cap In_B|/|In_B|", "wiki2vec sim", "BoW sim (1st par)", "docvec sim (1st par)",
                "title jaccard", "PMI", "LDA entropy A", "LDA entropy B", "LDA cross entropy A;B",
                "LDA cross entropy B;A", "# words A", "# words B", "# B appears in A",
                "# A appears in B", "# B appears in A (norm)", "# A appears in B (norm)",
                "# noun phrases A", "# noun phrases B", "# common noun phrases", "Hub_A - Hub_B",
                "Auth_A - Auth_B", "PageRank_A - PageRank_B]"]



def read_data(file_name):
    file = np.genfromtxt(file_name,delimiter=',')
    X = file[:-1]
    Y = file[-1]
    return X.T, Y


def evaluation_results(y_test, y_predict):
    accuracy = accuracy_score(y_test, y_predict)*100
    recall = recall_score(y_test, y_predict)*100
    precision = precision_score(y_test, y_predict)*100
    f1 = f1_score(y_test, y_predict)*100
    auc = roc_auc_score(y_test, y_predict)*100
    return [accuracy, precision, recall, f1, auc]


def print_results(file_name, method, result):
    print(file_name.split("/")[1].split(".")[0] + " with " + method)
    print("Accuracy: %.1f" % result[0])
    print("Precision: %.1f" % result[1])
    print("Recall: %.1f" % result[2])
    print("F1 Score: %.1f" % result[3])
    print("Area Under Curve: %.1f" % result[4])


def print_features(top_features):
    for i in top_features[:10]:
        print(feature_index[i])


def get_top_features(feature_score):
    feature_score = np.array(feature_score)
    top_features = np.argsort(feature_score)
    print_features(top_features)


def random_forest(x_train, x_test, y_train, y_test):
    rand_forest = RandomForestClassifier(max_depth = 200, random_state=0)
    rand_forest.fit(x_train, y_train)
    feature_score = rand_forest.feature_importances_
    get_top_features(feature_score)
    y_predict = rand_forest.predict(x_test)
    return evaluation_results(y_test, y_predict)


def k_fold_training(X, Y, model):
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size = 0.3, random_state = 0)
    if model == "NB":
        result = naive_bayes(x_train, x_test, y_train, y_test)
    elif model == "LR":
        result = logisitc_regression(x_train, x_test, y_train, y_test)
    elif model == "SVM":
        result = suppot_vaector_machine(x_train, x_test, y_train, y_test)
    elif model == "RF":
        result = random_forest(x_train, x_test, y_train, y_test)
    return result


def main_function(file_names, methods):
    for file_name in file_names:
        print(file_name)
        X, Y = read_data(file_name)
        for method in methods:
            results = k_fold_training(X, Y, model = method)
        print("\n")
main_function(file_names, methods)
