import pandas as pd


book_content_file = "../output_files/physics_normalized_content.csv"
labeled_pairs_file = "../output_files/physics_labeled_pairs.csv"
wikipedia_data_file = "../output_files/physics_correct_wikipedia_data.csv"
concepts_file = "../output_files/physics_concepts_ambiguity.csv"



def read_concepts_file():
    df = pd.read_csv(concepts_file, encoding = "utf-8")
    all_data = {}
    for i in range(df.shape[0]):
        all_data[i] = {
            "concept": df[["concept"]].iloc[i].values[0],
            "key_terms": df[["key_terms"]].iloc[i].values[0]
        }
    return all_data


def read_book_data():
    df = pd.read_csv(book_content_file, encoding = "utf-8")
    all_data = {}
    for i in range(df.shape[0]):
        if df[["content"]].iloc[i].isna().values[0]:
            content = ""
        else:
            content = df[["content"]].iloc[i].values[0]
        all_data[i] = {
            "section": df[["section"]].iloc[i].values[0],
            "title": df[["title"]].iloc[i].values[0],
            "page_no": df[["page_no"]].iloc[i].values[0],
            "content": content
        }
    return all_data


def read_labeled_pairs():
    df = pd.read_csv(labeled_pairs_file, encoding = "utf-8")
    all_data = {}
    for i in range(df.shape[0]):
        all_data[i] = {
            "topic_a": df[["topic_a"]].iloc[i].values[0],
            "topic_b": df[["topic_b"]].iloc[i].values[0],
            "relation": df[["relation"]].iloc[i].values[0],
        }
    return all_data


def read_wikipedia_data():
    df = pd.read_csv(wikipedia_data_file, encoding = "utf-8")
    all_data = {}
    for i in range(df.shape[0]):
        all_data[i] = {
            'topic': df[["topic"]].iloc[i].values[0],
            'wiki_title': df[["wiki_title"]].iloc[i].values[0],
            'wiki_summary': df[["wiki_summary"]].iloc[i].values[0],
            'wiki_content': df[["wiki_content"]].iloc[i].values[0],
            'wiki_links': df[["wiki_links"]].iloc[i].values[0],
        }
    return all_data


def read_concept_match(file_name):
    df = pd.read_csv(file_name, encoding = "utf-8")
    data = {}
    for i in range(df.shape[0]):
        concept = df[["concept"]].iloc[i].values[0]
        if df[["index"]].iloc[i].isna().values[0]:
            index = []
        else:
            index = df[["index"]].iloc[i].values[0].split("|")
        data[i] = {
            "concept" : concept,
            "index" : index,
            "type" : df[["type"]].iloc[i].values[0]
        }
    return data


#-------------------------------------------------------------------------#

# API for getting data from Wikipedia

def get_wiki_data(concept):
    wiki_data = read_wikipedia_data()
    for i in range(len(wiki_data)):
        title = wiki_data[i]["topic"]
        if title == concept:
            break
    summary = wiki_data[i]["wiki_summary"]
    content = wiki_data[i]["wiki_content"]
    return (summary, content)

# Get Book Section data

def get_section_data(book_data):
    section_list = [book_data[i]["section"] for i in range(len(book_data))]
    section_data = {}
    for i in range(len(section_list)):
        current_collection = [section_list[i]]
        flag = 0
        for j in range(i+1, len(section_list)):
            x1 = len(section_list[i].split("."))
            x2 = len(section_list[j].split("."))
            if x2 > x1:
                current_collection.append(section_list[j])
            else:
                section = section_list[i]
                section_data[section] = "|".join(current_collection)
                flag = 1
                break
        if flag == 0:
            section = section_list[i]
            section_data[section] = "|".join(current_collection)
            
        # if section_list[i] == '31':
            # section_data['31'] = "|".join(current_collection)

    return section_data


def get_data(book_data, section):
    for i in range(len(book_data)):
        if book_data[i]["section"] == section:
            break
    title = str(book_data[i]["title"])
    content = str(book_data[i]["content"])
    text = title + "\n" + content
    return text


def get_section_content(section, section_data, book_data):
    req_sections = section_data[section].split("|")
    content = ""
    for section in req_sections:
        content += get_data(book_data, section)
        content += "\n"
    return content


def get_book_data(section):
    book_data = read_book_data()
    section_data = get_section_data(book_data)
    # print(section_data)
    content = get_section_content(section, section_data, book_data)
    return content

# get_book_data('1')

# Get matched section data
