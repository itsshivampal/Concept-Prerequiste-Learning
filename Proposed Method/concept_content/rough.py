from load_data import *

# labeled_data = read_labeled_pairs()

# for i in range(len(labeled_data)):
#     if labeled_data[i]["topic_a"] == "Field (physics)":
#         print(labeled_data[i]["topic_a"], " : ", labeled_data[i]["topic_b"], labeled_data[i]["relation"])


import pandas as pd

file_name = "data/resolve_single_index.csv"
df = pd.read_csv(file_name, encoding = "utf-8")

df0 = df[df['type'] == 0]
df1 = df[df['type'] == 1].sort_values(by = ['single_score'])
df2 = df[df['type'] == 2].sort_values(by = ['single_score'])
df3 = df[df['type'] == 3].sort_values(by = ['single_score'])

df0.to_csv("data/sort_0_score.csv")
df1.to_csv("data/sort_1_score.csv")
df2.to_csv("data/sort_2_score.csv")
df3.to_csv("data/sort_3_score.csv")