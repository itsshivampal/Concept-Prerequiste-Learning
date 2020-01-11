'''

Following code is for getting prerequisite relations from the given concept space and datasets

import function "get_prereq_relations" in the file for using it

Use with following parameters:

get_prereq_relations(theta, all_topics, all_keyword_data, method, w_type, data_name)

theta: hyperparameter for tuning the prereq relations
all_topics: list of concept space
all_keyword_data: list of wikipedia data for those concepts
method: Method you are going to use like "refd"
w_type: tfidf or equal or any
data_name: CS or MATH or any other

'''




from library.save_data import *
import pandas as pd

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
        return 1
    else:
        return 0


# Calculation of W by "equal" w_type
def get_w_value_equal(topic_a, topic_b, all_keyword_data):
    referred_link_b = get_all_referred_links(topic_b, all_keyword_data)
    if topic_a in referred_link_b:
        return 1
    else:
        return 0


# Calculation of W by "tfidf" w_type
def get_w_value_tfidf(topic_a, topic_b, all_keyword_data):
    referred_link_b = get_all_referred_links(topic_b, all_keyword_data)
    if topic_a in referred_link_b:
        pass
    else:
        return 0


# Foloowing functions for RefD implementation
def part_a_calc(topic_a, topic_b, all_keyword_data, all_topics, w_type):
    part_a = 0.0
    if w_type == "equal":
        for topic in all_topics:
            part_a = part_a + get_r_value(topic, topic_b, all_keyword_data)*get_w_value_equal(topic, topic_a, all_keyword_data)
    elif w_type == "tfidf":
        for topic in all_topics:
            part_a = part_a + get_r_value(topic, topic_b, all_keyword_data)*get_w_value_tfidf(topic, topic_a, all_keyword_data)
    return float(part_a)


def part_b_calc(topic_a, all_keyword_data, all_topics, w_type):
    part_b = 0.0
    if w_type == "equal":
        for topic in all_topics:
            part_b = part_b + get_w_value_equal(topic, topic_a, all_keyword_data)
    elif w_type == "tfidf":
        for topic in all_topics:
            part_b = part_b + get_w_value_tfidf(topic, topic_a, all_keyword_data)
    return float(part_b)


def part_c_calc(topic_a, topic_b, all_keyword_data, all_topics, w_type):
    part_c = 0.0
    if w_type == "equal":
        for topic in all_topics:
            part_c = part_c + get_r_value(topic, topic_a, all_keyword_data)*get_w_value_equal(topic, topic_b, all_keyword_data)
    elif w_type == "tfidf":
        for topic in all_topics:
            part_c = part_c + get_r_value(topic, topic_a, all_keyword_data)*get_w_value_tfidf(topic, topic_b, all_keyword_data)
    return float(part_c)


def part_d_calc(topic_b, all_keyword_data, all_topics, w_type):
    part_d = 0.0
    if w_type == "equal":
        for topic in all_topics:
            part_d = part_d + get_w_value_equal(topic, topic_b, all_keyword_data)
    elif w_type == "tfidf":
        for topic in all_topics:
            part_d = part_d + get_w_value_tfidf(topic, topic_b, all_keyword_data)
    return float(part_d)


def refd_score_calc(topic_a, topic_b, all_keyword_data, all_topics, w_type):
    part_a = part_a_calc(topic_a, topic_b, all_keyword_data, all_topics, w_type)
    part_b = part_b_calc(topic_a, all_keyword_data, all_topics, w_type)
    part_c = part_c_calc(topic_a, topic_b, all_keyword_data, all_topics, w_type)
    part_d = part_d_calc(topic_b, all_keyword_data, all_topics, w_type)

    if part_b == 0 or part_d == 0:
        return 0
    else:
        RefD_a_b = (part_a/part_b) - (part_c/part_d)
        return RefD_a_b

# Ending of Refd Calculation method


#-------------------------------------------------------------------------------






#-------------------------------------------------------------------------------


def save_prereq_relation(data, method, w_type, data_name):
    column_name = ['topic_a', 'topic_b']
    location = "RefD Implementation/output_data/prereq_"
    location += data_name + "_" + method + "_" + w_type + ".csv"
    save_csv_data(location, data, column_name)


def score_calc_all_pairs(all_topics, all_keyword_data, method, w_type):
    all_pairs_refd_value = []
    for topic_a in all_topics:
        temp_topic = []
        for topic_b in all_topics:
            if method == "refd":
                refd_score = refd_score_calc(topic_a, topic_b, all_keyword_data, all_topics, w_type)
            temp_topic.append(refd_score)
        all_pairs_refd_value.append(temp_topic)
    return all_pairs_refd_value


def get_prereq_relations(theta, all_topics, all_keyword_data, method, w_type, data_name):
    prereq_results = {}
    count = 0
    theta_neg = -theta
    all_pairs_refd_value = score_calc_all_pairs(all_topics, all_keyword_data, method, w_type)
    for i in range(len(all_topics)):
        for j in range(len(all_topics)):
            if all_pairs_refd_value[i][j] > theta:
                data = {
                    "topic_a": all_topics[i],
                    "topic_b": all_topics[j]
                }
            elif all_pairs_refd_value[i][j] < theta_neg:
                data = {
                    "topic_a": all_topics[j],
                    "topic_b": all_topics[i]
                }
            else:
                continue
            prereq_results[count] = data
            count += 1
    save_prereq_relation(prereq_results, method, w_type, data_name)
    return prereq_results
