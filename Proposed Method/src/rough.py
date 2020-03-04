from load_data import *

labeled_data = read_labeled_pairs()

for i in range(len(labeled_data)):
    if labeled_data[i]["topic_a"] == "Potential energy":
        print(labeled_data[i]["topic_a"], " : ", labeled_data[i]["topic_b"], labeled_data[i]["relation"])
