from .save_data import save_json_data
from .data_reading import read_data, read_wiki_data
from .prereq_calculation import *



def get_term_frequency(topic_a, topic_b, all_keyword_data):
    topic_b_id = get_id(topic_b, all_keyword_data)
    data_b = all_keyword_data[topic_b_id]
    b_html_content = data_b["wiki_html"]
    b_soup = BeautifulSoup(b_html_content, 'html.parser').text
    term_frequency = b_soup.lower().count(topic_a.lower())
    return term_frequency


def get_idf(topic_a, all_keyword_data):
    n = len(all_keyword_data)
    count = 1
    for i in range(n):
        topic = all_keyword_data[i]["topic"]
        referred_links = all_keyword_data[i]["wiki_links"]
        if topic_a in referred_links: count += 1
    idf = math.log(n/count)
    return idf


def get_tfidf_value(topic_a, topic_b, all_keyword_data):
    referred_link_b = get_all_referred_links(topic_b, all_keyword_data)
    if topic_a in referred_link_b:
        tf = get_term_frequency(topic_a, topic_b, all_keyword_data)
        idf = get_idf(topic_a, all_keyword_data)
        tfidf = tf*idf
        return tfidf
    else:
        return 0.0


def get_all_tfidf_values(all_topics, all_keyword_data):
    tfidf_values = {}
    for topic_a in all_topics:
        data = {}
        for topic_b in all_topics:
            value = get_tfidf_value(topic_a, topic_b, all_keyword_data)
            data[topic_b] = value
        tfidf_values[topic_a] = data
    return tfidf_values


def save_tfidf_data(data, subject):
    file_name = "output_data/w_values/" + subject + "_tfidf.json"
    save_json_data(file_name, data)



def generate_tfidf_values(subject):
    df_pos, df_neg = read_data(subject)
    df_wiki = read_wiki_data(subject)

    all_topics = get_all_topics(df_pos, df_neg)
    all_keyword_data = get_keyword_wiki_data(df_wiki)

    tfidf_values = get_all_tfidf_values(all_topics, all_keyword_data)

    save_tfidf_data(tfidf_values, subject)

    print("TFIDF values created for ", subject)
