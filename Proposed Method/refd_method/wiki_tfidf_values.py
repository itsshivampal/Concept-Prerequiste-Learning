import pandas as pd
from bs4 import BeautifulSoup

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

        topic =  df[["topic"]].iloc[i].values[0],
        topic = topic[0]
        # print(topic[0])
        all_keyword_data[topic] = {
            'wiki_links': df[["wiki_links"]].iloc[i].values[0],
            'wiki_url': df[["wiki_url"]].iloc[i].values[0],
            'wiki_html': df[["wiki_html"]].iloc[i].values[0]
        }
    return all_keyword_data



def get_null_matrix(concept_list):
    data = {"concept": concept_list}
    for concept in concept_list:
        data[concept] = [0.0 for i in range(len(concept_list))]
    df = pd.DataFrame(data)
    df.set_index("concept", inplace = True)
    return df



def get_term_frequency(topic_a, topic_b, all_keyword_data):
    data_b = all_keyword_data[topic_b]
    b_html_content = data_b["wiki_html"]
    b_soup = BeautifulSoup(b_html_content, 'html.parser').text
    term_frequency = b_soup.lower().count(topic_a.lower())
    return term_frequency



def get_tf_matrix(concept_list, wiki_data):
    df = get_null_matrix(concept_list)
    for concept1 in concept_list:
        freq_sum = 0.0
        for concept2 in concept_list:
            freq = float(get_term_frequency(concept2, concept1, wiki_data))
            df.at[concept1, concept2] = freq
            freq_sum += freq
        for concept2 in concept_list:
            freq = df.at[concept1, concept2]
            if freq_sum != 0.0:
                df.at[concept1, concept2] = float(freq)/freq_sum
            else:
                df.at[concept1, concept2] = float(freq)
    return df




def get_idf(topic_a, all_keyword_data):
    n = len(all_keyword_data)
    count = 1
    for i in range(n):
        topic = all_keyword_data[i]["topic"]
        referred_links = all_keyword_data[i]["wiki_links"]
        if topic_a in referred_links: count += 1
    idf = math.log(n/count)
    return idf


def get_term_idf(concept_list, all_keyword_data):
    idf_data = {}
    for concept in concept_list:
        idf_data[concept] = get_idf(concept,all_keyword_data)
    return idf_data





def get_tf_idf_matrix(concept_list, df, idf_data):
    for concept1 in concept_list:
        for concept2 in concept_list:
            tf = df.loc[concept2, concept1]
            idf = idf_data[concept1]
            tf_idf = tf*idf
            df.at[concept2, concept1] = tf_idf
    return df



def generate_tfidf_values(prereq_file, wiki_data_file):
    df_prereq = pd.read_csv(prereq_file)
    df_wiki = pd.read_csv(wiki_data_file)

    concept_list = get_all_topics(df_prereq)
    all_keyword_data = get_keyword_wiki_data(df_wiki)

    df_term = get_tf_matrix(concept_list, all_keyword_data)
    idf_data = get_term_idf(concept_list, all_keyword_data)
    df_tfidf_matrix = get_tf_idf_matrix(concept_list, df_term, idf_data)

    print("tf-idf matrix done!")
    
    return df_tfidf_matrix



prereq_file = "../output_files/physics_labeled_pairs.csv"
wiki_data_file = "../output_files/physics_correct_wikipedia_data.csv"
df_tfidf_matrix = generate_tfidf_values(prereq_file, wiki_data_file)

output_file = "../output_files/wiki_tfidf_matrix.csv"
df_tfidf_matrix.to_csv(output_file)