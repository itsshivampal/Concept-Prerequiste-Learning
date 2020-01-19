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




def main_function(subject, theta, method, w_type):

    # Data Reading
    df_pos, df_neg = read_data(subject)
    df_wiki = read_wiki_data(subject)

    # get prerequisite relations for the given parameters
    df_estimated = get_prereq_relations(df_pos, df_neg, df_wiki,
                                                theta, method, w_type, subject)
    print(check_opp_pairs(df_estimated))

    # save calculated prerequisite data
    # save_prereq_relation(df_estimated, method, w_type, subject, theta)

    # estimated result evaluation
    estimated_results = evaluate_prereq_estimation(df_pos, df_neg, df_estimated)

    # save evaluation results
    # save_evaluation_results(estimated_results, method, w_type, subject, theta)

    return estimated_results



subject = "CS"
method = "refd"
w_type = "tfidf"
optimize_theta(subject, method, w_type)


subject = "CS"
method = "refd"
w_type = "equal"
optimize_theta(subject, method, w_type)


subject = "MATH"
method = "refd"
w_type = "tfidf"
optimize_theta(subject, method, w_type)


subject = "MATH"
method = "refd"
w_type = "equal"
optimize_theta(subject, method, w_type)


#-----------------------------------------------------------------------------------
# Following function is for getting value at particular instance

# subject = "CS"
# method = "refd"
# w_type = "tfidf"
# theta = 0.02
# estimated_results = main_function(subject, theta, method, w_type)
# print(estimated_results)




















#
#
#
#
#
# from library.prereq_calculation import *
#
# df_pos, df_neg = read_data(subject)
#
# all_topics = get_all_topics(df_pos, df_neg)
#
#
# subject = "CS"
#
#
#
#
#
# # get_w_value_tfidf(topic_a, topic_b, tfidf_values)
#
# for topic_a in all_topics:
#     for topic_b in all_topics:
#         print(data[topic_a][topic_b])
