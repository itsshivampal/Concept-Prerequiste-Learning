import pandas as pd


# Data Reading
# Reading files from Course Dataset for CS
file1 = "RefD Implementation/RefD_dataset/Course/CS.edges"
file2 = "RefD Implementation/RefD_dataset/Course/CS.edges_neg"

f1 = open(file1)
f2 = open(file2)

all_topics = []

for line in f1:
    keywords = line.strip().split("\t")
    all_topics.append(keywords[0])
    all_topics.append(keywords[1])

for line in f2:
    keywords = line.strip().split("\t")
    all_topics.append(keywords[0])
    all_topics.append(keywords[1])

all_topics = list(set(all_topics))

# Reading data from CSV files
df = pd.read_csv("RefD Implementation/output_data/keyterms_wiki_data.csv", encoding="utf-8")
topic = df[["topic"]]
wiki_links = df[["wiki_links"]]
index_length = df.shape[0]
wiki_links.iloc[18].values[0] = ""
all_keyword_data = {}

for i in range(index_length):
    all_keyword_data[i] = {
        'topic': topic.iloc[i].values[0],
        'wiki_links': wiki_links.iloc[i].values[0]
    }

# End Reading Data

# RefD code implementation
def get_id(topic):
    for i in all_keyword_data:
        if all_keyword_data[i]["topic"] == topic:
            break
    return i


def get_all_referred_links(topic):
    topic_id = get_id(topic)
    referred_links = all_keyword_data[topic_id]["wiki_links"]
    return referred_links


def get_r_value(topic_a, topic_b):
    referred_link_a = get_all_referred_links(topic_a)
    if topic_b in referred_link_a:
        return 1
    else:
        return 0


def get_w_value_equal(topic_a, topic_b):
    referred_link_b = get_all_referred_links(topic_b)
    if topic_a in referred_link_b:
        return 1
    else:
        return 0


def get_w_value_tfidf(topic_a, topic_b):
    pass

# Foloowing functions for RefD implementation

def part_a_calc(topic_a, topic_b):
    part_a = 0.0
    for topic in all_topics:
        part_a = part_a + get_r_value(topic, topic_b)*get_w_value_equal(topic, topic_a)
    return float(part_a)


def part_b_calc(topic_a, topic_b):
    part_b = 0
    for topic in all_topics:
        part_b = part_b + get_w_value_equal(topic, topic_a)
    return float(part_b)


def part_c_calc(topic_a, topic_b):
    part_c = 0
    for topic in all_topics:
        part_c = part_c + get_r_value(topic, topic_a)*get_w_value_equal(topic, topic_b)
    return float(part_c)


def part_d_calc(topic_a, topic_b):
    part_d = 0
    for topic in all_topics:
        part_d = part_d + get_w_value_equal(topic, topic_b)
    return float(part_d)


def refd_score_calc(topic_a, topic_b):
    part_a = part_a_calc(topic_a, topic_b)
    part_b = part_b_calc(topic_a, topic_b)
    part_c = part_c_calc(topic_a, topic_b)
    part_d = part_d_calc(topic_a, topic_b)

    if part_b == 0 or part_d == 0:
        return 0
    else:
        RefD_a_b = (part_a/part_b) - (part_c/part_d)
        return RefD_a_b


all_pairs_refd_value = []

for topic_a in all_topics:
    temp_topic = []
    for topic_b in all_topics:
        refd_score = refd_score_calc(topic_a, topic_b)
        temp_topic.append(refd_score)
    all_pairs_refd_value.append(temp_topic)

prereq_a = []
prereq_b = []

theta = 0.02
theta_neg = -0.02

for i in range(len(all_topics)):
    for j in range(len(all_topics)):
        if all_pairs_refd_value[i][j] > theta:
            prereq_b.append(all_topics[j])
            prereq_a.append(all_topics[i])
        elif all_pairs_refd_value[i][j] < theta_neg:
            prereq_b.append(all_topics[i])
            prereq_a.append(all_topics[j])
        else:
            continue

prereq_results = {}

for i in range(len(prereq_a)):
    prereq_results[i] = {
        "topic_a": prereq_a[i],
        "topic_b": prereq_b[i]
    }


# Exporting all results in CSV format

df = pd.DataFrame(columns=['topic_a', 'topic_b'])

for i in range(len(prereq_results)):
    df = df.append(prereq_results[i], ignore_index=True)

df.to_csv("RefD Implementation/output_data/prereq_matches.csv")
