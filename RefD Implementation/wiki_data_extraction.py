from library.extract_wiki_data import *
from library.save_data import *

import pandas as pd
import wikipedia
import json
import random
import os


# Step 0: Reading files from Course Dataset for CS
file1 = "RefD Implementation/RefD_dataset/Course/CS.edges"
file2 = "RefD Implementation/RefD_dataset/Course/CS.edges_neg"

f1 = open(file1)
f2 = open(file2)

all_cs_topics = []

for line in f1:
    keywords = line.strip().split("\t")
    all_cs_topics.append(keywords[0])
    all_cs_topics.append(keywords[1])

for line in f2:
    keywords = line.strip().split("\t")
    all_cs_topics.append(keywords[0])
    all_cs_topics.append(keywords[1])

all_cs_topics = list(set(all_cs_topics))
print(len(all_cs_topics))

#---------------------------------------------------------------------

# Step 0: Reading files from Course Dataset for Math
file1 = "RefD Implementation/RefD_dataset/Course/MATH.edges"
file2 = "RefD Implementation/RefD_dataset/Course/MATH.edges_neg"

f1 = open(file1)
f2 = open(file2)

all_math_topics = []

for line in f1:
    keywords = line.strip().split("\t")
    all_math_topics.append(keywords[0])
    all_math_topics.append(keywords[1])

for line in f2:
    keywords = line.strip().split("\t")
    all_math_topics.append(keywords[0])
    all_math_topics.append(keywords[1])

all_math_topics = list(set(all_math_topics))
print(len(all_math_topics))

#---------------------------------------------------------------------

# Step 1: Extracting wikipedia data for CS Dataset
def extract_cs_data(all_cs_keyword_data):
    all_cs_keyword_data = get_list_wiki_data(all_cs_topics)
    location_cs = "RefD Implementation/output_data/CS_wiki_data.csv"
    wiki_params = wiki_data_list()
    save_csv_data(location_cs, all_cs_keyword_data, wiki_params)
    return True

#----------------------------------------------------------------------

# Step 1: Extracting wikipedia data for MATH Dataset
def extract_math_data(all_math_keyword_data):
    all_math_keyword_data = get_list_wiki_data(all_math_topics)
    location_math = "RefD Implementation/output_data/MATH_wiki_data.csv"
    wiki_params = wiki_data_list()
    save_csv_data(location_math, all_math_keyword_data, wiki_params)
    return True

#----------------------------------------------------------------------


extract_cs_data(all_cs_topics)
print("cs data extracted\n")
extract_math_data(all_math_topics)
print("math data extracted\n")
