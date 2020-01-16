from library.save_data import save_csv_data, save_evaluation_results, save_prereq_relation
from library.data_reading import read_data, read_wiki_data
from library.algorithm_evaluation import evaluate_prereq_estimation
from library.prereq_calculation import get_prereq_relations
import pandas as pd


# Define all required parameters here
subject = "CS"
theta = 0.02
method = "refd"
w_type = "equal"



def main_function(subject, theta, method, w_type):

    # Data Reading
    df_pos, df_neg = read_data(subject)
    df_wiki = read_wiki_data(subject)

    # get prerequisite relations for the given parameters
    df_estimated = get_prereq_relations(df_pos, df_neg, df_wiki,
                                                theta, method, w_type, subject)
    # save calculated prerequisite data
    save_prereq_relation(df_estimated, method, w_type, subject, theta)

    # estimated result evaluation
    estimated_results = evaluate_prereq_estimation(df_pos, df_neg, df_estimated)

    # save evaluation results
    save_evaluation_results(estimated_results, method, w_type, subject, theta)

    return estimated_results


estimated_results = main_function(subject, theta, method, w_type)

print(estimated_results)
