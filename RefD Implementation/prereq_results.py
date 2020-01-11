from library.save_data import *
from library.prereq_calculation import get_prereq_relations
import pandas as pd





file1 = "RefD Implementation/RefD_dataset/Course/CS.edges"
f1 = open(file1)
all_topics = []
for line in f1:
    keywords = line.strip().split("\t")
    all_topics.append(keywords[0])
    all_topics.append(keywords[1])

all_topics = list(set(all_topics))

df = pd.read_csv("RefD Implementation/output_data/final_CS_wiki_data.csv", encoding="utf-8")
topic = df[["topic"]]
wiki_links = df[["wiki_links"]]
index_length = df.shape[0]

all_keyword_data = {}

for i in range(index_length):
    all_keyword_data[i] = {
        'topic': topic.iloc[i].values[0],
        'wiki_links': wiki_links.iloc[i].values[0]
    }

# End Reading Data

print(len(all_keyword_data))
print(len(all_topics))


get_prereq_relations(0.02, all_topics, all_keyword_data, "refd", "equal", "CS")
