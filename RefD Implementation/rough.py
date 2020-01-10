import pandas as pd
import wikipedia

# Data Reading
# Reading files from Course Dataset for CS
# file1 = "RefD Implementation/RefD_dataset/Course/CS.edges"
# file2 = "RefD Implementation/RefD_dataset/Course/CS.edges_neg"
#
# f1 = open(file1)
# f2 = open(file2)
#
# all_topics = []
#
# for line in f1:
#     keywords = line.strip().split("\t")
#     all_topics.append(keywords[0])
#     all_topics.append(keywords[1])
#
# for line in f2:
#     keywords = line.strip().split("\t")
#     all_topics.append(keywords[0])
#     all_topics.append(keywords[1])
#
# all_topics = list(set(all_topics))
#
# # Reading data from CSV files
# df = pd.read_csv("RefD Implementation/output_data/keyterms_wiki_data.csv", encoding="utf-8")
# topic = df[["topic"]]
# wiki_links = df[["wiki_links"]]
# title = df[["wiki_title"]]
#
# index_length = df.shape[0]
# print(index_length)
#
# wiki_links.iloc[18].values[0] = ""
# all_keyword_data = {}
#
# for i in range(index_length):
#     all_keyword_data[i] = {
#         'topic': topic.iloc[i].values[0],
#         'wiki_links': wiki_links.iloc[i].values[0]
#     }
#
# # End Reading Data
#
#
# count = 0
# for i in range(index_length):
#     if topic.iloc[i].values[0] == title.iloc[i].values[0]:
#         count += 1
#     else:
#         print(topic.iloc[i].values[0], "\t", title.iloc[i].values[0])
#
# print(count)


print(wikipedia.search("Parallel Processing")[0])
