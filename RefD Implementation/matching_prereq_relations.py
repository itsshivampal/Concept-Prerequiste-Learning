import pandas as pd
import wikipedia
import random
import os


# Reading files from Course Dataset for CS
file1 = "RefD Implementation/RefD_dataset/Course/CS.edges"
file2 = "RefD Implementation/RefD_dataset/Course/CS.edges_neg"
prereq_file = "RefD Implementation/output_data/prereq_matches.csv"

def read_file(file_name):
    file = open(file_name)
    all_pairs = {}
    i = 0
    for line in file:
        keywords = line.strip().split("\t")
        all_pairs[i] = {
            "topic_a": keywords[0],
            "topic_b": keywords[1]
        }
        i += 1
    df = pd.DataFrame(columns=['topic_a', 'topic_b'])
    for i in range(len(all_pairs)):
        df = df.append(all_pairs[i], ignore_index=True)
    return df

df_cs_edge = read_file(file1)
df_cs_edge_neg = read_file(file2)
# df_cs_edge_neg = df_cs_edge_neg.drop_duplicates()

# Reading calculated prerequisite relation file
df_prereq_match = pd.read_csv(prereq_file, encoding = "utf-8")


def read_csv_file(df):
    topic_pair_list = {}
    index_length = df.shape[0]
    for i in range(index_length):
        topic_pair_list[i] = {
            'topic_a': df[["topic_a"]].iloc[i].values[0],
            'topic_b': df[["topic_b"]].iloc[i].values[0]
        }
    return topic_pair_list

def swap_cols_csv(df):
    topic_pair_list = {}
    index_length = df.shape[0]
    for i in range(index_length):
        topic_pair_list[i] = {
            'topic_a': df[["topic_b"]].iloc[i].values[0],
            'topic_b': df[["topic_a"]].iloc[i].values[0]
        }
    return topic_pair_list

def match_row(x1, x2):
    if x1["topic_a"] == x2["topic_a"] and x1["topic_b"] == x2["topic_b"]:
        return True
    else:
        return False

def match_two_tables(df1, df2):
    count = 0
    len1 = len(df1)
    len2 = len(df2)
    for i in range(len1):
        flag = False
        for j in range(len2):
            if match_row(df1[i], df2[j]): flag = True
        if flag: count += 1
    return count

def check_row_repetition(df):
    set1 = read_csv_file(df)
    set2 = swap_cols_csv(df)
    count = match_two_tables(set1, set2)
    return count

def check_similar_rows(df1, df2):
    set1 = read_csv_file(df1)
    set2 = read_csv_file(df2)
    count = match_two_tables(set1, set2)
    return count

# Output Presentation
print("No of rows in cs edge dataset: ", df_cs_edge.shape[0])
print("No of rows in cs edge negative dataset: ", df_cs_edge_neg.shape[0])
print("No of rows in calculated prereq calculation dataset: ", df_prereq_match.shape[0])
print("\n")

# matching of similar columns in calculated prerequistes file
print("No of repeated rows in prereq calculated file: ", check_row_repetition(df_prereq_match))
print("No of repeated rows in cs edge file: ", check_row_repetition(df_cs_edge))
print("No of repeated rows in cs edge negative file: ", check_row_repetition(df_cs_edge_neg))
print("\n")

# matching original dataset with out calculated dataset
print("No of same rows in cs_edge and prereq_cal file: ", check_similar_rows(df_cs_edge, df_prereq_match))
print("No of same rows in cs_edge_neg and prereq_cal file: ", check_similar_rows(df_cs_edge_neg, df_prereq_match))
