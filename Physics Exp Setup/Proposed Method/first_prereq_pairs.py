import pandas as pd
import numpy as np


def get_tfidf_val(c1, c2, concept_index, df_val):
    ind1 = concept_index[c1]
    ind2 = concept_index[c2]
    col1 = df_val[ind1,:]
    col2 = df_val[:,ind2]
    arr = []
    for i in range(len(col1)):
        val_temp = min(col1[i], col2[i])
        arr.append(val_temp)
    return max(arr)


def get_first_prereq_pairs(df):
    concept_list = df["concept"].values
    df.set_index("concept", inplace = True)
    df_final = df
    df_val = df.values
    print(df_val.shape)

    concept_index = {concept_list[i] : i for i in range(0, len(concept_list))}

    #  First pass of finding prereq pairs
    for c1 in concept_list:
        for c2 in concept_list:
            val = df_final.at[c1, c2]
            if val == 0.0:
                df_final.at[c1, c2] = get_tfidf_val(c1, c2, concept_index, df_val)

    # 2nd pass of finding prereq pairs
    # df = df_final
    # df_val = df.values
    #
    # for c1 in concept_list:
    #     for c2 in concept_list:
    #         val = df_final.at[c1, c2]
    #         if val == 0.0:
    #             df_final.at[c1, c2] = get_tfidf_val(c1, c2, concept_index, df_val)

    return df_final
