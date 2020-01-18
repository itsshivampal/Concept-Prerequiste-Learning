from library.save_data import save_csv_data, save_evaluation_results, save_prereq_relation
from library.data_reading import read_data, read_wiki_data
from library.algorithm_evaluation import evaluate_prereq_estimation, check_opp_pairs
from library.prereq_calculation import get_prereq_relations
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_plotting(x_label, y_label):
    plt.plot(x_label, y_label)
    plt.xlabel('theta_values')
    plt.ylabel('average_values')
    plt.title('Accuracy measures')
    plt.show()


def optimize_theta(subject, method, w_type):
    theta_values = [float("{0:.2f}".format((0.0 + 0.01*i))) for i in range(100)]
    average_values = []
    for theta in theta_values:
        estimated_results = main_function(subject, theta, method, w_type)
        average_values.append(estimated_results["accuracy"])
        print(theta, estimated_results["accuracy"])
    get_plotting(average_values, theta_values)




def main_function(subject, theta, method, w_type):

    # Data Reading
    df_pos, df_neg = read_data(subject)
    df_wiki = read_wiki_data(subject)

    # get prerequisite relations for the given parameters
    df_estimated = get_prereq_relations(df_pos, df_neg, df_wiki,
                                                theta, method, w_type, subject)
    # print(df_estimated.shape[0])
    # print(check_opp_pairs(df_estimated))
    # save calculated prerequisite data
    # save_prereq_relation(df_estimated, method, w_type, subject, theta)

    # estimated result evaluation
    estimated_results = evaluate_prereq_estimation(df_pos, df_neg, df_estimated)

    # save evaluation results
    # save_evaluation_results(estimated_results, method, w_type, subject, theta)

    return estimated_results


# Define all required parameters here
subject = "CS"
theta = 0.98
method = "refd"
w_type = "equal"

# optimize_theta(subject, method, w_type)



estimated_results = main_function(subject, theta, method, w_type)

print(estimated_results)
