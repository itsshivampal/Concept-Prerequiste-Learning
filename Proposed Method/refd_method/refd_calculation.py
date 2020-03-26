
import pandas as pd
from bs4 import BeautifulSoup
import math


# Functions for reading data

def get_all_topics(df):
    all_topics = []

    for i in range(df.shape[0]):
        all_topics.append(df[["topic_a"]].iloc[i].values[0])
        all_topics.append(df[["topic_b"]].iloc[i].values[0])

    all_topics = list(set(all_topics))
    return all_topics


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



#-------------------------------------------------------------------------------

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



def get_w_value_tfidf(topic_a, topic_b, tfidf_values):
    return tfidf_values.at[topic_a, topic_b]




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


def refd_score(topic_a, topic_b, all_keyword_data, all_topics, tfidf_values):
    w_type = "equal"
    equal_refd_score = refd_score_calc(topic_a, topic_b, all_keyword_data, all_topics, w_type, tfidf_values)

    w_type = "tfidf"
    tfidf_refd_score = refd_score_calc(topic_a, topic_b, all_keyword_data, all_topics, w_type, tfidf_values)

    return equal_refd_score, tfidf_refd_score

# Ending of Refd Calculation method


#-------------------------------------------------------------------------------



def get_prereq_relations(df_prereq, df_wiki, tfidf_values):
    all_topics = get_all_topics(df_prereq)
    all_keyword_data = get_keyword_wiki_data(df_wiki)

    # for i in range(df_prereq.shape[0]):
    for i in range(10):
        print(i)
        topic_a = df_prereq[["topic_a"]].iloc[i].values[0]
        topic_b = df_prereq[["topic_b"]].iloc[i].values[0]

        refd_equal, refd_tfidf = refd_score(topic_a, topic_b, all_keyword_data, all_topics, tfidf_values)

        df_prereq.at[i, "refd_equal"] = refd_equal
        df_prereq.at[i, "refd_tfidf"] = refd_tfidf

    return df_prereq


def main_function(prereq_file, wiki_data_file, tfidf_file):
    df_prereq = pd.read_csv(prereq_file)
    df_wiki = pd.read_csv(wiki_data_file)
    df_tfidf = pd.read_csv(tfidf_file)
    df_tfidf.set_index("concept", inplace = True)

    df_estimated = get_prereq_relations(df_prereq, df_wiki, tfidf_values)
    return df_estimated



prereq_file = "../output_files/physics_labeled_pairs.csv"
wiki_data_file = "../output_files/physics_correct_wikipedia_data.csv"
tfidf_file = "../output_files/wiki_tfidf_matrix.csv"

df_estimated = main_function(prereq_file, wiki_data_file, tfidf_file)

output_file = "../output_files/refd_estimated_results.csv"
df_estimated.to_csv(output_file)


