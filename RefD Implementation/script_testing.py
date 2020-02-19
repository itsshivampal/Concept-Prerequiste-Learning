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


##################################################################################################


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

#####################################################################################################




#####################################################################################################

# Useful functions of RefD calculation

def get_id(topic, all_keyword_data):
    for i in all_keyword_data:
        if all_keyword_data[i]["topic"] == topic:
            break
    return i


def get_all_referred_links(topic, all_keyword_data):
    topic_id = get_id(topic, all_keyword_data)
    referred_links = all_keyword_data[topic_id]["wiki_links"][1:-1]
    referred_links = referred_links.split(",")
    links = [referred_links[0][1:-1]]
    for i in range(1, len(referred_links)):
        links.append(referred_links[i][2:-1])
    return links


def read_tfidf_json_data(subject):
    filename = "output_data/w_values/" + subject + "_tfidf.json"
    with open(filename) as f:
        data = json.load(f)
    return data

##################################################################################################





#-------------------------------------------------------------------------------


def get_common_links(referred_links, all_topics):
    topics = [topic for topic in referred_links if topic in all_topics]
    return topics



def score_calc_pairs(all_topics, all_keyword_data, method, w_type):
    if w_type == "tfidf":
        tfidf_values = read_tfidf_json_data(data_name)
    else:
        tfidf_values = {}

    topic_a = "Algorithm"
    topic_b = "Discrete mathematics"

    # topic_a = "Computer architecture"
    # topic_b = "Microarchitecture"

    print("Referred links of topic - ", topic_a)
    links_a = get_all_referred_links(topic_a, all_keyword_data)
    links_a = get_common_links(links_a, all_topics)
    for link in links_a: print(link)
    print("\n")


    print("Referred links of topic - ", topic_b)
    links_b = get_all_referred_links(topic_b, all_keyword_data)
    links_b = get_common_links(links_b, all_topics)
    for link in links_b: print(link)
    print("\n")


    count_a = 0
    count_b = 0

    for link in links_a:
        referred_links = get_all_referred_links(link, all_keyword_data)
        if topic_b in referred_links:
            count_a += 1
            print(link)
    print("\n")

    for link in links_b:
        referred_links = get_all_referred_links(link, all_keyword_data)
        if topic_a in referred_links:
            count_b += 1
            print(link)
    print("\n")

    print(len(links_a))
    print(len(links_b))
    print(count_a)
    print(count_b)

    return 0



def get_prereq_relations(df_pos, df_neg, df_wiki, theta, method, w_type):
    all_topics = get_all_topics(df_pos, df_neg)
    print("Following is the list of all topics")
    for topic in all_topics: print(topic)
    print("\n")

    all_keyword_data = get_keyword_wiki_data(df_wiki)
    refd_score = score_calc_pairs(all_topics, all_keyword_data, method, w_type)
    return refd_score


def main_function(subject, method, w_type):
    df_pos, df_neg = read_data(subject)
    df_wiki = read_wiki_data(subject)
    estimated = get_prereq_relations(df_pos, df_neg, df_wiki,
                                             method, w_type, subject)
    return estimated



subject = "CS"
method = "refd"
w_type = "equal"
main_function(subject, method, w_type)
