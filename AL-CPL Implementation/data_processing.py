import pandas as pd
import numpy as np



columns = ["f0", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9",
            "f10", "f11", "f12", "f13", "f14", "f15", "f16", "f17", "f18", "f19",
            "f20", "f21", "f22", "f23", "f24", "f25", "f26", "f27", "f28", "f29",
            "f30", "f31", "f32", "f33", "f34", "f35", "f36", "f37", "output"]


def extract_data(line):
    features = line.split()
    data = {
        "output" : int(features[0]),
        "f0" : float(features[1].split(":")[1]),
        "f1" : float(features[2].split(":")[1]),
        "f2" : float(features[3].split(":")[1]),
        "f3" : float(features[4].split(":")[1]),
        "f4" : float(features[5].split(":")[1]),
        "f5" : float(features[6].split(":")[1]),
        "f6" : float(features[7].split(":")[1]),
        "f7" : float(features[8].split(":")[1]),
        "f8" : float(features[9].split(":")[1]),
        "f9" : float(features[10].split(":")[1]),
        "f10" : float(features[11].split(":")[1]),
        "f11" : float(features[12].split(":")[1]),
        "f12" : float(features[13].split(":")[1]),
        "f13" : float(features[14].split(":")[1]),
        "f14" : float(features[15].split(":")[1]),
        "f15" : float(features[16].split(":")[1]),
        "f16" : float(features[17].split(":")[1]),
        "f17" : float(features[18].split(":")[1]),
        "f18" : float(features[19].split(":")[1]),
        "f19" : float(features[20].split(":")[1]),
        "f20" : float(features[21].split(":")[1]),
        "f21" : float(features[22].split(":")[1]),
        "f22" : float(features[23].split(":")[1]),
        "f23" : float(features[24].split(":")[1]),
        "f24" : float(features[25].split(":")[1]),
        "f25" : float(features[26].split(":")[1]),
        "f26" : float(features[27].split(":")[1]),
        "f27" : float(features[28].split(":")[1]),
        "f28" : float(features[29].split(":")[1]),
        "f29" : float(features[30].split(":")[1]),
        "f30" : float(features[31].split(":")[1]),
        "f31" : float(features[32].split(":")[1]),
        "f32" : float(features[33].split(":")[1]),
        "f33" : float(features[34].split(":")[1]),
        "f34" : float(features[35].split(":")[1]),
        "f35" : float(features[36].split(":")[1]),
        "f36" : float(features[37].split(":")[1]),
        "f37" : float(features[38].split(":")[1]),
    }
    return data


def normalize_array(x):
    x = np.array(x)
    min_x = np.min(x)
    max_x = np.max(x)
    x = (x - min_x)/(max_x - min_x)
    return x


def normalized_df(df):
    X = [normalize_array([df[[col]].values[i][0] for i in range(len(df[[col]]))]) for col in columns]
    X = np.array(X)
    return X


def file_read(file_name):
    file_location = "dataset/" + file_name
    file = open(file_location, "r")
    df = pd.DataFrame(columns = columns)
    for line in file:
        df = df.append(extract_data(line), ignore_index=True)
    data = normalized_df(df)
    np.savetxt("output/" + file_name.split(".")[0] + ".csv", data, delimiter = ",")


def generate_csv_data(file_names):
    for file_name in file_names:
        file_read(file_name)



#     Converting given data to csv format     #
file_names = ["data_mining.features", "geometry.features", "physics.features", "precalculus.features"]
generate_csv_data(file_names)
