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

methods = ["NB", "LR", "SVM", "RF"]

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
    print("\n")


def naive_bayes(x_train, x_test, y_train, y_test):
    gaussian_nb = GaussianNB()
    gaussian_nb.fit(x_train, y_train)
    y_predict = gaussian_nb.predict(x_test)
    # print(y_predict)
    return evaluation_results(y_test, y_predict)


def logisitc_regression(x_train, x_test, y_train, y_test):
    logistic_reg = LogisticRegression(solver='lbfgs') # C=1.0, default. solver="lbfgs", default
    logistic_reg.fit(x_train, y_train)
    y_predict = logistic_reg.predict(x_test)
    # print(y_predict)
    return evaluation_results(y_test, y_predict)


def suppot_vaector_machine(x_train, x_test, y_train, y_test):
    support_vector = LinearSVC(random_state=0, tol=1e-5)
    support_vector.fit(x_train, y_train)
    y_predict = support_vector.predict(x_test)
    # print(y_predict)
    return evaluation_results(y_test, y_predict)


def random_forest(x_train, x_test, y_train, y_test):
    rand_forest = RandomForestClassifier(max_depth = 200, random_state=0)
    rand_forest.fit(x_train, y_train)
    y_predict = rand_forest.predict(x_test)
    # print(y_predict)
    return evaluation_results(y_test, y_predict)


def k_fold_training(X, Y, model):
    # x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size = 0.3, random_state = 0)
    results = []
    kf = KFold(n_splits = 5)
    kf.get_n_splits(X)
    for train_index, test_index in kf.split(X):
        x_train, x_test = X[train_index], X[test_index]
        y_train, y_test = Y[train_index], Y[test_index]
        if model == "NB":
            result = naive_bayes(x_train, x_test, y_train, y_test)
        elif model == "LR":
            result = logisitc_regression(x_train, x_test, y_train, y_test)
        elif model == "SVM":
            result = suppot_vaector_machine(x_train, x_test, y_train, y_test)
        elif model == "RF":
            result = random_forest(x_train, x_test, y_train, y_test)
        results.append(result)
    results = np.array(results)
    final_result = np.mean(results, axis = 0)
    return final_result



def main_function(file_names, methods):
    for file_name in file_names:
        X, Y = read_data(file_name)
        for method in methods:
            results = k_fold_training(X, Y, model = method)
            print_results(file_name, method, results)

main_function(file_names, methods)
