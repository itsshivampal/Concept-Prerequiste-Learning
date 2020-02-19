from library.save_data import save_csv_data, save_evaluation_results, save_prereq_relation, save_plots
from library.data_reading import read_data, read_wiki_data
from library.algorithm_evaluation import evaluate_prereq_estimation, check_opp_pairs
from library.prereq_calculation import get_prereq_relations
from library.save_tfidf_values import generate_tfidf_values
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import math


#---------------------------------------------------------------------------------
# Following functions are for generating tfidf values for given subjects

# generate_tfidf_values("CS")
# generate_tfidf_values("MATH")

#---------------------------------------------------------------------------------


def optimize_theta(subject, method, w_type):
    theta_values = [float("{0:.2f}".format((0.0 + 0.01*i))) for i in range(100)]
    accuracy_values = []
    precision_values = []
    recall_values = []
    f1_values = []
    for theta in theta_values:
        estimated_results = main_function(subject, theta, method, w_type)
        accuracy_values.append(estimated_results["accuracy"])
        precision_values.append(estimated_results["precision"])
        recall_values.append(estimated_results["recall"])
        f1_values.append(estimated_results["f1_score"])
        print(theta, estimated_results)
    save_plots(subject, w_type, theta_values, accuracy_values, precision_values, recall_values, f1_values)




# def main_function(subject, theta, method, w_type):
#
#     # Data Reading
#     df_pos, df_neg = read_data(subject)
#     df_wiki = read_wiki_data(subject)
#
#     # get prerequisite relations for the given parameters
#     df_estimated = get_prereq_relations(df_pos, df_neg, df_wiki,
#                                                 theta, method, w_type, subject)
#     print(check_opp_pairs(df_estimated))
#
#     # save calculated prerequisite data
#     # save_prereq_relation(df_estimated, method, w_type, subject, theta)
#
#     # estimated result evaluation
#     estimated_results = evaluate_prereq_estimation(df_pos, df_neg, df_estimated)
#
#     # save evaluation results
#     # save_evaluation_results(estimated_results, method, w_type, subject, theta)
#
#     return estimated_results



# subject = "CS"
# method = "refd"
# w_type = "tfidf"
# optimize_theta(subject, method, w_type)
#
#
# subject = "CS"
# method = "refd"
# w_type = "equal"
# optimize_theta(subject, method, w_type)
#
#
# subject = "MATH"
# method = "refd"
# w_type = "tfidf"
# optimize_theta(subject, method, w_type)
#
#
# subject = "MATH"
# method = "refd"
# w_type = "equal"
# optimize_theta(subject, method, w_type)


#-----------------------------------------------------------------------------------
# Following function is for getting value at particular instance

def main_function(subject, method, w_type, theta):

    # Data Reading
    df_pos, df_neg = read_data(subject)
    df_wiki = read_wiki_data(subject)

    # get prerequisite relations for the given parameters
    df_estimated = get_prereq_relations(df_pos, df_neg, df_wiki,
                                                theta, method, w_type, subject)

    return df_estimated
    # print(check_opp_pairs(df_estimated))

    # save calculated prerequisite data
    # save_prereq_relation(df_estimated, method, w_type, subject, theta)

    # estimated result evaluation
    # estimated_results = evaluate_prereq_estimation(df_pos, df_neg, df_estimated)

    # save evaluation results
    # save_evaluation_results(estimated_results, method, w_type, subject, theta)

    # return estimated_results



# subject = "MATH"
# method = "refd"
# w_type = "equal"
# theta = 0.05
# estimated_results = main_function(subject, method, w_type, theta)
# estimated_results.to_csv("math_equal_results.csv")
# print(estimated_results)




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
        estimated = y_estimate.iloc[i].values[0]
        truth = y_truth.iloc[i].values[0]
        result = check_state(estimated, theta)
        score_state = compare_result(result, truth)
        if score_state == 1: TP += 1
        elif score_state == 2: FN += 1
        elif score_state == 3: FP += 1
        elif score_state == 4: TN += 1
    print(TP, FN, FP, TN)
    data = estimation_measures(TP, FN, FP, TN)
    return data


def check_accuracy_measures(file_name, theta):
    df = pd.read_csv(file_name, encoding = "utf-8")
    y_estimate = df[["estimated"]]
    y_truth = df[["ground_truth"]]
    data = check_estimation(y_estimate, y_truth, theta)
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



def optimize_theta(file_name):

    theta_values = [float("{0:.2f}".format((0.0 + 0.01*i))) for i in range(100)]
    accuracy_values = []
    precision_values = []
    recall_values = []
    f1_values = []
    for theta in theta_values:
        estimated_results = check_accuracy_measures(file_name, theta)
        accuracy_values.append(estimated_results["accuracy"])
        precision_values.append(estimated_results["precision"])
        recall_values.append(estimated_results["recall"])
        f1_values.append(estimated_results["f1_score"])
        print(theta, estimated_results)
    plots_checking(theta_values, accuracy_values, precision_values, recall_values, f1_values)


# file_name = "cs_equal_results.csv"
# theta = 0.05
# data = check_accuracy_measures(file_name, theta)
# print(data)


file_name = "math_equal_results.csv"
optimize_theta(file_name)
