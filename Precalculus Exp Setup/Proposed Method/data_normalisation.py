import pandas as pd
import numpy as np


# def book_name_correction(concept_list, df):
# 	for concept in concept_list:
# 		df.at[concept, "Geometry"] = 1.0
# 	for concept in concept_list:
# 		df.at["Geometry", concept] = 0.0
# 	return df


def normalise_data(df):
    concept_list = df["concept"].values
    df.set_index("concept", inplace = True)
    column_maxes = df.max()
    df_max = column_maxes.max()

    column_mins = df.min()
    df_min = column_mins.min()

    normal_df = df/df_max

    # df = book_name_correction(concept_list, df)

    return df
