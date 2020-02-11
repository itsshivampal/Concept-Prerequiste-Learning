'''

Following code is for getting prerequisite relations from the given concept space and datasets

import function "get_prereq_relations" in the file for using it

Use with following parameters:

get_prereq_relations(theta, all_topics, all_keyword_data, method, w_type, data_name)

theta: hyperparameter for tuning the prereq relations
prereq_data: file name of file containg prereq relations of a subject
wiki_data: file name of file containing wikipedia data for prereq_data keywords
method: Method you are going to use like "refd"
w_type: tfidf or equal or any
data_name: CS or MATH or any other

'''




from library.save_data import *
import pandas as pd
from bs4 import BeautifulSoup
import math


# Functions for reading data

def get_all_topics(df_pos, df_neg):
    all_topics = []

    for i in range(df_pos.shape[0]):
        all_topics.append(df_pos[["topic_a"]].iloc[i].values[0])
        all_topics.append(df_pos[["topic_b"]].iloc[i].values[0])

    for i in range(df_neg.shape[0]):
        all_topics.append(df_neg[["topic_a"]].iloc[i].values[0])
        all_topics.append(df_neg[["topic_b"]].iloc[i].values[0])

    all_topics = list(set(all_topics))
    return all_topics


def get_pairs(df):
    all_pairs = {}
    index = 0
    for i in range(df.shape[0]):
        all_pairs[i] = {
            "topic_a": df[["topic_a"]].iloc[i].values[0],
            "topic_b": df[["topic_b"]].iloc[i].values[0]
        }
    return all_pairs


def get_keyword_wiki_data(df):
    all_keyword_data = {}
    for i in range(df.shape[0]):
        all_keyword_data[i] = {
            'topic': df[["topic"]].iloc[i].values[0],
            'wiki_links': df[["wiki_links"]].iloc[i].values[0],
            'wiki_url': df[["wiki_url"]].iloc[i].values[0],
            'wiki_html': df[["wiki_html"]].iloc[i].values[0]
        }
    return all_keyword_data


# remove duplicate rows and coulmns in calculated dataset
def remove_duplicates(df):
    df = df.drop_duplicates(subset = ['topic_a', 'topic_b'], keep = "first")
    indexNames = df[df['topic_a'] == df['topic_b']].index
    if indexNames.size > 0:
        df.drop(indexNames, inplace = True)
    return df



# Useful functions of RefD calculation

def get_id(topic, all_keyword_data):
    for i in all_keyword_data:
        if all_keyword_data[i]["topic"] == topic:
            break
    return i


def get_all_referred_links(topic, all_keyword_data):
    topic_id = get_id(topic, all_keyword_data)
    referred_links = all_keyword_data[topic_id]["wiki_links"]
    return referred_links


def get_r_value(topic_a, topic_b, all_keyword_data):
    referred_link_a = get_all_referred_links(topic_a, all_keyword_data)
    if topic_b in referred_link_a:
        return 1.0
    else:
        return 0.0


# Calculation of W by "equal" w_type
def get_w_value_equal(topic_a, topic_b, all_keyword_data):
    referred_link_b = get_all_referred_links(topic_b, all_keyword_data)
    if topic_a in referred_link_b:
        return 1.0
    else:
        return 0.0


def read_tfidf_json_data(subject):
    filename = "output_data/w_values/" + subject + "_tfidf.json"
    with open(filename) as f:
        data = json.load(f)
    return data



def get_w_value_tfidf(topic_a, topic_b, tfidf_values):
    return tfidf_values[topic_a][topic_b]




# Following functions for RefD implementation
def part_a_calc(topic_a, topic_b, all_keyword_data, all_topics, w_type, tfidf_values):
    part_a = 0.0
    if w_type == "equal":
        for topic in all_topics:
            part_a = part_a + get_r_value(topic, topic_b, all_keyword_data)*get_w_value_equal(topic, topic_a, all_keyword_data)
    elif w_type == "tfidf":
        for topic in all_topics:
            part_a = part_a + get_r_value(topic, topic_b, all_keyword_data)*get_w_value_tfidf(topic, topic_a, tfidf_values)
    return float(part_a)


def part_b_calc(topic_a, all_keyword_data, all_topics, w_type, tfidf_values):
    part_b = 0.0
    if w_type == "equal":
        for topic in all_topics:
            part_b = part_b + get_w_value_equal(topic, topic_a, all_keyword_data)
    elif w_type == "tfidf":
        for topic in all_topics:
            part_b = part_b + get_w_value_tfidf(topic, topic_a, tfidf_values)
    return float(part_b)


def part_c_calc(topic_a, topic_b, all_keyword_data, all_topics, w_type, tfidf_values):
    part_c = 0.0
    if w_type == "equal":
        for topic in all_topics:
            part_c = part_c + get_r_value(topic, topic_a, all_keyword_data)*get_w_value_equal(topic, topic_b, all_keyword_data)
    elif w_type == "tfidf":
        for topic in all_topics:
            part_c = part_c + get_r_value(topic, topic_a, all_keyword_data)*get_w_value_tfidf(topic, topic_b, tfidf_values)
    return float(part_c)


def part_d_calc(topic_b, all_keyword_data, all_topics, w_type, tfidf_values):
    part_d = 0.0
    if w_type == "equal":
        for topic in all_topics:
            part_d = part_d + get_w_value_equal(topic, topic_b, all_keyword_data)
    elif w_type == "tfidf":
        for topic in all_topics:
            part_d = part_d + get_w_value_tfidf(topic, topic_b, tfidf_values)
    return float(part_d)


def refd_score_calc(topic_a, topic_b, all_keyword_data, all_topics, w_type, tfidf_values):
    part_a = part_a_calc(topic_a, topic_b, all_keyword_data, all_topics, w_type, tfidf_values)
    part_b = part_b_calc(topic_a, all_keyword_data, all_topics, w_type, tfidf_values)
    part_c = part_c_calc(topic_a, topic_b, all_keyword_data, all_topics, w_type, tfidf_values)
    part_d = part_d_calc(topic_b, all_keyword_data, all_topics, w_type, tfidf_values)

    if part_b == 0 or part_d == 0:
        return 0
    else:
        RefD_a_b = (part_a/part_b) - (part_c/part_d)
        return RefD_a_b

# Ending of Refd Calculation method


#-------------------------------------------------------------------------------






#-------------------------------------------------------------------------------


def dict_to_csv(data):
    df = pd.DataFrame(columns = ["topic_a", "topic_b", "ground_truth", "estimated"])
    for i in range(len(data)):
        df = df.append(data[i], ignore_index=True)
    df = remove_duplicates(df)
    return df



def score_calc_pairs(pairs, all_topics, all_keyword_data, method, w_type, data_name):
    all_pairs_refd_value = []
    if w_type == "tfidf":
        tfidf_values = read_tfidf_json_data(data_name)
    else:
        tfidf_values = {}

    for i in range(len(pairs)):
        pair = pairs[i]
        topic_a = pair["topic_a"]
        topic_b = pair["topic_b"]
        if method == "refd":
            refd_score = refd_score_calc(topic_a, topic_b, all_keyword_data, all_topics, w_type, tfidf_values)
            all_pairs_refd_value.append(refd_score)
    return all_pairs_refd_value


def merge_results(pos_pairs, neg_pairs, pos_refd_value, neg_refd_value):
    all_data = {}
    index = 0
    for i in range(len(pos_pairs)):
        all_data[index] = {
            "topic_a": pos_pairs[i]["topic_a"],
            "topic_b": pos_pairs[i]["topic_b"],
            "ground_truth": 1,
            "estimated": pos_refd_value[i]
        }
        index += 1

    for i in range(len(neg_pairs)):
        all_data[index] = {
            "topic_a": neg_pairs[i]["topic_a"],
            "topic_b": neg_pairs[i]["topic_b"],
            "ground_truth": 0,
            "estimated": neg_refd_value[i]
        }
        index += 1
    return all_data







def get_prereq_relations(df_pos, df_neg, df_wiki, theta, method, w_type, data_name):
    all_topics = get_all_topics(df_pos, df_neg)
    all_keyword_data = get_keyword_wiki_data(df_wiki)
    df_pos_pairs = get_pairs(df_pos)
    df_neg_pairs = get_pairs(df_neg)

    df_pos_pairs_refd = score_calc_pairs(df_pos_pairs, all_topics, all_keyword_data, method, w_type, data_name)
    df_neg_pairs_refd = score_calc_pairs(df_neg_pairs, all_topics, all_keyword_data, method, w_type, data_name)

    overall_results = merge_results(df_pos_pairs, df_neg_pairs, df_pos_pairs_refd, df_neg_pairs_refd)

    df_results = dict_to_csv(overall_results)

    return df_results
