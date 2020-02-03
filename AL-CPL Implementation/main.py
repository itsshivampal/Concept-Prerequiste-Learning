import pandas as pd
import numpy as np


# Data Reading
file_name = "output/data_mining.csv"

def read_data(file_name):
    file = np.genfromtxt(file_name,delimiter=',')
    X = file[:-1]
    Y = file[-1]
    return X, Y

X, Y = read_data(file_name)
