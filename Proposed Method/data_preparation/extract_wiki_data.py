'''
Extracting Wikipedia Content

For using this library, import extract_wikipedia_data
and use function - extract_wikipedia_data(topic)
for extracting wikipedia data for that topic
'''

import pandas as pd
import wikipedia
import random
import os

import wikipedia

def contain_section(line):
    line = line.strip()
    if len(line) > 4:
        if line[0] == "=" and line[1] == "=" and line[-2] == "=" and line[-1] == "=":
            return True
        else:
            return False


def wiki_section_extract(content):
    lines = content.split("\n")
    sections = ""
    for line in lines:
        if contain_section(line):
            sections += line[3:-3] + "\n"
    return sections.strip()


def keyword_data(topic = "", wiki_title = "", wiki_url = "",
                wiki_summary = "", wiki_content = "",
                wiki_html = "", wiki_links = "", wiki_sections = ""):
    data = {
        'topic': topic,
        "wiki_title": wiki_title,
        "wiki_url": wiki_url,
        "wiki_summary": wiki_summary,
        "wiki_content": wiki_content,
        "wiki_html": wiki_html,
        "wiki_links": wiki_links,
        "wiki_sections": wiki_sections
    }
    return data


def wiki_data_list():
    wiki_list = ['topic', 'wiki_title', "wiki_url", 'wiki_summary', 'wiki_content', 'wiki_html', 'wiki_links', 'wiki_sections']
    return wiki_list


def extract_wikipedia_data(topic):
    wiki_title = ""
    wiki_url = ""
    wiki_summary = ""
    wiki_content = ""
    wiki_html = ""
    wiki_links = ""
    wiki_sections = ""
    try:
        wiki = wikipedia.search(topic)[0]
        try:
            wiki_data = wikipedia.page(wiki)
            wiki_title = wiki_data.title
            wiki_url = wiki_data.url.split("/")[-1]
            wiki_summary = wiki_data.summary
            wiki_content = wiki_data.content
            wiki_html = wiki_data.html()
            wiki_links = wiki_data.links
            wiki_sections = wiki_section_extract(wiki_content)

        except wikipedia.exceptions.DisambiguationError as e:
            print("blank")
        except wikipedia.exceptions.PageError as e:
            print("blank")

    except IndexError:
        print("blank")

    data = keyword_data(topic, wiki_title, wiki_url, wiki_summary,
                        wiki_content, wiki_html, wiki_links, wiki_sections)
    return data


def get_list_wiki_data(all_keywords):
    list_len = len(all_keywords)
    all_keyword_data = {}
    for i in range(list_len):
        all_keyword_data[i] = extract_wikipedia_data(all_keywords[i])
        print(i, all_keyword_data[i]["topic"])
    return all_keyword_data


def save_wiki_data(wikipedia_data, output_file):
    df = pd.DataFrame(columns = wiki_data_list())
    for i in range(len(wikipedia_data)):
        df = df.append(wikipedia_data[i], ignore_index = True)
    df.to_csv(output_file)
    return True


def extract_wiki_data(concepts_file, output_file):
    df = pd.read_csv(concepts_file)
    concepts = df["topic"].tolist()
    wikipedia_data = get_list_wiki_data(concepts)
    save_wiki_data(wikipedia_data, output_file)
    return True


concepts_file = "output/physics_concepts.csv"
output_file = "output/physics_wikipedia_data.csv"


# Following function is for extracting data from wikipedia library
# extract_wiki_data(concepts_file, output_file)



title_correction = {
    0: {
        "topic": "Angle of incidence",
        "title": "Angle of incidence (optics)"
    },
    1: {
        "topic": "Friction",
        "title": "Friction (physics)"
    },
    2: {
        "topic": "Electric charge",
        "title": "Electric charge (physics)"
    },
    3: {
        "topic": "Dielectric",
        "title": "Dielectric (physics)"
    },
    4: {
        "topic": "Planet",
        "title": "Planets (moving body)"
    },
    5: {
        "topic": "Lever",
        "title": "Lever (Physics)"
    },
    6: {
        "topic": "Electron",
        "title": "Electron (Physics)"
    },
    7: {
        "topic": "Magnetism",
        "title": "Magnetism (magnetized)"
    }
}


def correct_dataset(df, correction):
    for i in range(len(correction)):
        for j in range(df.shape[0]):
            topic = df[["topic"]].iloc[j].values[0]
            if topic == correction[i]["topic"]:
                index = j
                break
        wiki = wikipedia.page(correction[i]["title"])
        print(index, df[["topic"]].iloc[index].values[0], wiki.title)
        data = {
            "topic": df[["topic"]].iloc[index].values[0],
            "wiki_title": wiki.title,
            "wiki_url": wiki.url,
            "wiki_summary": wiki.summary,
            "wiki_content": wiki.content,
            "wiki_html": wiki.html(),
            "wiki_links": wiki.links,
            "wiki_sections": wiki_section_extract(wiki.content),
        }
        df = df.drop(df.index[index])
        df = df.append(data, ignore_index = True)
    return df


def correct_extracted_dataset(file_name, updated_file):
    df = pd.read_csv(file_name, encoding = "utf-8")
    df = correct_dataset(df, title_correction)
    df.to_csv(updated_file)
    return True

original_file = output_file
updated_file = "output/physics_correct_wikipedia_data.csv"

# correct_extracted_dataset(original_file, updated_file)
