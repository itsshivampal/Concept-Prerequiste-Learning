import pandas as pd

def read_data(dtype):
    if dtype == "CS":
        # file_pos = "RefD Implementation/output_data/CS_edge.csv"
        # file_neg = "RefD Implementation/output_data/CS_edge_neg.csv"
        file_pos = "output_data/CS_edge.csv"
        file_neg = "output_data/CS_edge_neg.csv"
        df_pos = pd.read_csv(file_pos, encoding = "utf-8")
        df_neg = pd.read_csv(file_neg, encoding = "utf-8")
    elif dtype == "MATH":
        # file_pos = "RefD Implementation/output_data/MATH_edge.csv"
        # file_neg = "RefD Implementation/output_data/MATH_edge_neg.csv"
        file_pos = "output_data/MATH_edge.csv"
        file_neg = "output_data/MATH_edge_neg.csv"
        df_pos = pd.read_csv(file_pos, encoding = "utf-8")
        df_neg = pd.read_csv(file_neg, encoding = "utf-8")
    return (df_pos, df_neg)


def read_wiki_data(dtype):
    if dtype == "CS":
        # file_wiki = "RefD Implementation/output_data/final_CS_wiki_data.csv"
        file_wiki = "output_data/final_CS_wiki_data.csv"
        df_wiki = pd.read_csv(file_wiki, encoding = "utf-8")
    elif dtype == "MATH":
        # file_wiki = "RefD Implementation/output_data/final_MATH_wiki_data.csv"
        file_wiki = "output_data/final_MATH_wiki_data.csv"
        df_wiki = pd.read_csv(file_wiki, encoding = "utf-8")
    return df_wiki
