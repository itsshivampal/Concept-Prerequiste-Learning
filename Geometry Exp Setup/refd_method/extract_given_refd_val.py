import pandas as pd
import numpy as np

def extract_data(line):
    features = line.split()
    data = {
        "output" : int(features[0]),
        "refd_val" : float(features[11].split(":")[1]),
    }
    return data


def normalize_array(x):
    x = np.array(x)
    min_x = np.min(x)
    max_x = np.max(x)
    x = (x - min_x)/(max_x - min_x)
    return x


def file_read(file_name):
    file_location = file_name
    file = open(file_location, "r")
    df = pd.DataFrame(columns = ["refd_val", "output"])
    for line in file:
        df = df.append(extract_data(line), ignore_index=True)
    return df

#     Converting given data to csv format     #
file_name = "../../dataset/geometry.features"
df = file_read(file_name)

output_file = "../../result_analysis/refd_given_vals.csv"

df.to_csv(output_file)
