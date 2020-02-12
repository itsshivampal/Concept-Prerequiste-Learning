import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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




columns = ["f0", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9",
            "f10", "f11", "f12", "f13", "f14", "f15", "f16", "f17", "f18", "f19",
            "f20", "f21", "f22", "f23", "f24", "f25", "f26", "f27", "f28", "f29",
            "f30", "f31", "f32", "f33", "f34", "f35", "f36", "f37", "output"]


def extract_data(line):
    features = line.split()
    data = {
        "output" : int(features[0]),
        "f0" : float(features[1].split(":")[1]),
        "f1" : float(features[2].split(":")[1]),
        "f2" : float(features[3].split(":")[1]),
        "f3" : float(features[4].split(":")[1]),
        "f4" : float(features[5].split(":")[1]),
        "f5" : float(features[6].split(":")[1]),
        "f6" : float(features[7].split(":")[1]),
        "f7" : float(features[8].split(":")[1]),
        "f8" : float(features[9].split(":")[1]),
        "f9" : float(features[10].split(":")[1]),
        "f10" : float(features[11].split(":")[1]),
        "f11" : float(features[12].split(":")[1]),
        "f12" : float(features[13].split(":")[1]),
        "f13" : float(features[14].split(":")[1]),
        "f14" : float(features[15].split(":")[1]),
        "f15" : float(features[16].split(":")[1]),
        "f16" : float(features[17].split(":")[1]),
        "f17" : float(features[18].split(":")[1]),
        "f18" : float(features[19].split(":")[1]),
        "f19" : float(features[20].split(":")[1]),
        "f20" : float(features[21].split(":")[1]),
        "f21" : float(features[22].split(":")[1]),
        "f22" : float(features[23].split(":")[1]),
        "f23" : float(features[24].split(":")[1]),
        "f24" : float(features[25].split(":")[1]),
        "f25" : float(features[26].split(":")[1]),
        "f26" : float(features[27].split(":")[1]),
        "f27" : float(features[28].split(":")[1]),
        "f28" : float(features[29].split(":")[1]),
        "f29" : float(features[30].split(":")[1]),
        "f30" : float(features[31].split(":")[1]),
        "f31" : float(features[32].split(":")[1]),
        "f32" : float(features[33].split(":")[1]),
        "f33" : float(features[34].split(":")[1]),
        "f34" : float(features[35].split(":")[1]),
        "f35" : float(features[36].split(":")[1]),
        "f36" : float(features[37].split(":")[1]),
        "f37" : float(features[38].split(":")[1]),
    }
    return data


def normalize_array(x):
    x = np.array(x)
    min_x = np.min(x)
    max_x = np.max(x)
    x = (x - min_x)/(max_x - min_x)
    return x


def normalized_df(df):
    X = [normalize_array([df[[col]].values[i][0] for i in range(len(df[[col]]))]) for col in columns]
    X = np.array(X)
    return X


def file_read(file_name):
    file_location = "dataset/" + file_name
    file = open(file_location, "r")
    df = pd.DataFrame(columns = columns)
    for line in file:
        df = df.append(extract_data(line), ignore_index=True)
    return df




# Data Reading



def read_data(file_name):
    file = np.genfromtxt(file_name,delimiter=',')
    X = file[:-1]
    # X = X.T
    y_truth = file[-1]
    estimated = X[10]
    return y_truth, estimated


def check_state(val, theta):
    if val >= theta: return 1
    else: return 0


def compare_result(result, truth):
    if truth == 1:
        if result == 1: return 1
        elif result == 0: return 2
    elif truth == 0:
        if result == 1: return 3
        elif result == 0: return 4


def estimation_measures(TP, FN, FP, TN):
    precision = TP/(TP + FP)
    recall = TP/(TP + FN)
    accuracy = (TP)/(TP + FN + FP)
    if precision == 0 and recall == 0:
        f1_score = 0
    else:
        f1_score = 2*precision*recall/(precision + recall)
    data = {
        "precision": precision,
        "recall": recall,
        "accuracy": accuracy,
        "f1_score": f1_score
    }
    return data


def estimation_measures(TP, FN, FP, TN):
    if TP == 0 and FP == 0:
        precision = 0
    else:
        precision = TP/(TP + FP)

    if TP == 0 and FN == 0:
        recall = 0
    else:
        recall = TP/(TP + FN)

    accuracy = (TP + TN)/(TP + FN + FP + TN)

    if precision == 0 and recall == 0:
        f1_score = 0
    else:
        f1_score = 2*precision*recall/(precision + recall)
    data = {
        "precision": precision,
        "recall": recall,
        "accuracy": accuracy,
        "f1_score": f1_score
    }
    return data



def check_estimation(y_estimate, y_truth, theta):
    TP = 0
    TN = 0
    FN = 0
    FP = 0
    for i in range(y_estimate.shape[0]):
        estimated = y_estimate[i]
        truth = y_truth[i]
        result = check_state(estimated, theta)
        score_state = compare_result(result, truth)
        if score_state == 1: TP += 1
        elif score_state == 2: FN += 1
        elif score_state == 3: FP += 1
        elif score_state == 4: TN += 1
    print(TP, FN, FP, TN)
    data = estimation_measures(TP, FN, FP, TN)
    return data




def plots_checking(theta_values, accuracy_values, precision_values, recall_values, f1_values):
    location = "results/"

    plt.plot(theta_values, accuracy_values)
    plt.xlabel('theta')
    plt.ylabel('accuracy')
    file_name = location + "theta_v_accuracy.png"
    plt.savefig(file_name)
    plt.clf()

    plt.plot(theta_values, precision_values)
    plt.xlabel('theta')
    plt.ylabel('precision')
    file_name = location + "theta_v_precision.png"
    plt.savefig(file_name)
    plt.clf()

    plt.plot(theta_values, recall_values)
    plt.xlabel('theta')
    plt.ylabel('recall')
    file_name = location + "theta_v_recall.png"
    plt.savefig(file_name)
    plt.clf()

    plt.plot(theta_values, f1_values)
    plt.xlabel('theta')
    plt.ylabel('f1_score')
    file_name = location + "theta_v_f1Score.png"
    plt.savefig(file_name)
    plt.clf()

    plt.plot(recall_values, precision_values)
    plt.xlabel('recall')
    plt.ylabel('precision')
    file_name = location + "precision_v_recall.png"
    plt.savefig(file_name)
    plt.clf()



def optimize_theta(y_estimate, y_truth):
    theta_values = [float("{0:.2f}".format((0.0 + 0.01*i))) for i in range(100)]
    accuracy_values = []
    precision_values = []
    recall_values = []
    f1_values = []
    for theta in theta_values:
        estimated_results = check_estimation(y_estimate, y_truth, theta)
        accuracy_values.append(estimated_results["accuracy"])
        precision_values.append(estimated_results["precision"])
        recall_values.append(estimated_results["recall"])
        f1_values.append(estimated_results["f1_score"])
        print(theta, estimated_results)
    plots_checking(theta_values, accuracy_values, precision_values, recall_values, f1_values)



# file_names = "output/data_mining.csv"
file_names = "data_mining.features"
df = file_read(file_names)
ground_truth = df[["output"]]
y_truth = [ground_truth.iloc[i].values[0] for i in range(df.shape[0])]
y_truth = np.array(y_truth)
estimated = df[["f10"]]
y_estimate = [estimated.iloc[i].values[0] for i in range(df.shape[0])]
y_estimate = np.array(y_estimate)

print(np.max(y_estimate))
print(np.min(y_estimate))


# optimize_theta(y_truth, y_estimate)
# theta = 0.05
# data = check_estimation(y_estimate, y_truth, theta)
# print(data)

# print(y_estimate)

# print(df[["f10"]])
