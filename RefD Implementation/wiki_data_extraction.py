import pandas as pd
import wikipedia
import json
import random
import os


# ## Reading files from Course Dataset for CS
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


# Extracting Wikipedia Content
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

def keyword_data(topic = "", wiki_title = "", wiki_summary = "",
                 wiki_content = "", wiki_html = "", wiki_links = "", wiki_sections = ""):
    data = {
        'topic': topic,
        "wiki_title": wiki_title,
        "wiki_summary": wiki_summary,
        "wiki_content": wiki_content,
        "wiki_html": wiki_html,
        "wiki_links": wiki_links,
        "wiki_sections": wiki_sections
    }
    return data


def extract_data(topic):
    wiki_title = ""
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


    data = keyword_data(topic, wiki_title, wiki_summary,
                        wiki_content, wiki_html, wiki_links, wiki_sections)

    return data

# Data Extraction
list_len = len(all_topics)
all_keyword_data = {}

complete = 0
for i in range(list_len - complete):
    i += complete
    data = extract_data(all_topics[i])
    all_keyword_data[i] = data
    print(i)


# Saving data in JSON Format
with open('output_data/keyterms_wiki_data.json', 'w') as file:
    json.dump(all_keyword_data, file)

## Saving data in CSV format
df = pd.DataFrame(columns=['topic', 'abbreviation', 'wiki_title', 'wiki_summary', 'wiki_content', 'wiki_html', 'wiki_links', 'wiki_sections'])

for i in range(len(all_keyword_data)):
    df = df.append(all_keyword_data[i], ignore_index=True)

df.to_csv("output_data/keyterms_wiki_data.csv")
