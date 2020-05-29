import pandas as pd
import numpy as np


def normalise_data(df):
    df.set_index("concept", inplace = True)
    column_maxes = df.max()
    df_max = column_maxes.max()

    column_mins = df.min()
    df_min = column_mins.min()

    normal_df = df/df_max
    
    return df
