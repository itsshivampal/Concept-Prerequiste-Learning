import pandas as pd
import os

replace_cs_strings = {
    'Algorithm design': 'Algorithm',
    'Compiler construction': 'Compiler',
    'Mobile application development': 'Mobile app development',
    'System programming': 'Systems programming',
    'Parallel processing': 'Parallel processing (DSP implementation)'
}


def remove_duplicates(df):
    df = df.drop_duplicates(subset = ['topic_a', 'topic_b'], keep = "first")
    return df


def text_to_df(file_name):
    df = pd.DataFrame(columns = ['topic_a', 'topic_b'])
    file = open(file_name)
    for line in file:
        keywords = line.strip().split("\t")
        data = {
            'topic_a': keywords[0],
            'topic_b': keywords[1]
        }
        df = df.append(data, ignore_index=True)
    return df


def replace_cs_keywords(df):
    total_size = df.shape[0]
    for i in range(total_size):
        text1 = df[["topic_a"]].iloc[i].values[0]
        text2 = df[["topic_b"]].iloc[i].values[0]
        if text1 in replace_cs_strings:
            df.loc[i, "topic_a"] = replace_cs_strings[text1]
        if text2 in replace_cs_strings:
            df.loc[i, "topic_b"] = replace_cs_strings[text2]
    return df


file1 = "RefD Implementation/RefD_dataset/Course/CS.edges"
file2 = "RefD Implementation/RefD_dataset/Course/CS.edges_neg"
file3 = "RefD Implementation/RefD_dataset/Course/MATH.edges"
file4 = "RefD Implementation/RefD_dataset/Course/MATH.edges_neg"

# Save CS.edges Dataset
df_cs_edge = text_to_df(file1)
df_cs_edge = replace_cs_keywords(df_cs_edge)
df_cs_edge = remove_duplicates(df_cs_edge)
df_cs_edge.to_csv("RefD Implementation/output_data/CS_edge.csv")

# Save CS.edges_neg Dataset
df_cs_edge_neg = text_to_df(file2)
df_cs_edge_neg = replace_cs_keywords(df_cs_edge_neg)
df_cs_edge_neg = remove_duplicates(df_cs_edge_neg)
df_cs_edge_neg.to_csv("RefD Implementation/output_data/CS_edge_neg.csv")

# # Save MATH.edges Dataset
df_math_edge = text_to_df(file3)
df_math_edge = remove_duplicates(df_math_edge)
df_math_edge.to_csv("RefD Implementation/output_data/MATH_edge.csv")

# # Save MATH.edges_neg Dataset
df_math_edge_neg = text_to_df(file4)
df_math_edge_neg = remove_duplicates(df_math_edge_neg)
df_math_edge_neg.to_csv("RefD Implementation/output_data/MATH_edge_neg.csv")
