from library.extract_wiki_data import *
from library.save_data import *

import pandas as pd
import wikipedia
import json
import random
import os


# Scanning of wikipedia datasets
df_math = pd.read_csv("RefD Implementation/output_data/MATH_wiki_data.csv", encoding="utf-8")
df_cs = pd.read_csv("RefD Implementation/output_data/CS_wiki_data.csv", encoding="utf-8")

def scan_dataset(df):
    topic = df[["topic"]]
    title = df[["wiki_title"]]
    index_length = df.shape[0]
    count = 0
    for i in range(index_length):
        if topic.iloc[i].values[0] == title.iloc[i].values[0]:
            count += 1
        else:
            print(i, topic.iloc[i].values[0], "\t", title.iloc[i].values[0])
    print("No of rows of same topic and title: ", count)
    print("No of rows of diff topic and title: ", index_length - count)

# Correction need to made in MATH dataset
math_correction = {
    0: {
        "index": 51,
        "title": "C star algebra"
    },
    1: {
        "index": 20,
        "title": "K theory"
    }
}

# Correction need to made in CS dataset
cs_correction = {
    0: {
        "index": 18,
        "title": "Parallel processing (DSP implementation)"
    }
}


def get_status(keyword):
    print("\n")
    print(wikipedia.search(keyword))
    print(wikipedia.page(keyword).title)

def correct_dataset(df, correction):
    for i in range(len(correction)):
        index = correction[i]["index"]
        wiki = wikipedia.page(correction[i]["title"])
        data = {
            "topic": df[["topic"]].iloc[index].values[0],
            "wiki_title": wiki.title,
            "wiki_summary": wiki.summary,
            "wiki_content": wiki.content,
            "wiki_html": wiki.html(),
            "wiki_links": wiki.links,
            "wiki_sections": wiki_section_extract(wiki.content),
        }
        df = df.drop(df.index[index])
        df = df.append(data, ignore_index = True)
    return df

def update_math_dataset(df_math):
    print("Original status of MATH dataset")
    scan_dataset(df_math)
    df_math = correct_dataset(df_math, math_correction)
    print("\nCurrent Status of Math Dataset")
    scan_dataset(df_math)
    df_math.to_csv("RefD Implementation/output_data/final_MATH_wiki_data.csv")
    return True

def update_cs_dataset(df_cs):
    print("\nOriginal status of CS dataset")
    scan_dataset(df_cs)
    df_cs = correct_dataset(df_cs, cs_correction)
    print("\nCurrent Status of Math Dataset")
    scan_dataset(df_cs)
    df_cs.to_csv("RefD Implementation/output_data/final_CS_wiki_data.csv")
    return True


# Functions for updating both the datasets
update_math_dataset(df_math)
update_cs_dataset(df_cs)
