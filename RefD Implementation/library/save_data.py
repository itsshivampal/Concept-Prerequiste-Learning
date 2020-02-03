'''
Following functions are for saving dataset in JSON and CSV formats

For saving data in JSON, pass (output_file, data) in save_json_data
For saving data in CSV, pass (output_file, data, parameters) in save_csv_data

output_file: location with filename and extension
data: should be in dictionary format
parameters: should be in array containing all the column names
'''

import json
import pandas as pd
import matplotlib.pyplot as plt



# Saving data in JSON Format
def save_json_data(output_file, data):
    with open(output_file, 'w') as file:
        json.dump(data, file)
    return True


## Saving data in CSV format
def save_csv_data(output_file, data, parameters):
    df = pd.DataFrame(columns = parameters)
    for i in range(len(data)):
        df = df.append(data[i], ignore_index=True)
    df.to_csv(output_file)
    return True


def save_prereq_relation(df, method, w_type, data_name, theta):
    location = "RefD Implementation/output_data/calculated_prereq/" + data_name + "/"
    location += method + "_" + w_type + "_" + str(int(theta*100)) + ".csv"
    df.to_csv(location)
    return True


def save_evaluation_results(data, method, w_type, data_name, theta):
    location = "RefD Implementation/output_data/calculated_prereq/" + data_name + "/"
    location += method + "_" + w_type + "_" + str(int(theta*100)) + ".txt"
    file = open(location, "w+")
    line = "Accuracy: " + str(data["accuracy"]) + "\n"
    file.write(line)
    line = "Precision: " + str(data["precision"]) + "\n"
    file.write(line)
    line = "Recall: " + str(data["recall"]) + "\n"
    file.write(line)
    line = "F1 Score: " + str(data["f1_score"]) + "\n"
    file.write(line)
    file.close()
    return True


def save_plots(subject, w_type, theta_values, accuracy_values, precision_values, recall_values, f1_values):
    location = "RefD Implementation/results/" + subject + "/" + w_type + "/"

    plt.plot(theta_values, accuracy_values)
    plt.xlabel('theta')
    plt.ylabel('accuracy')
    file_name = location + "theta_v_accuracy.png"
    plt.savefig(file_name)
    plt.clf()

    plt.plot(theta_values, precision_values)
    plt.xlabel('theta')
    plt.ylabel('precision')
    file_name = location + "theta_v_precision.png"
    plt.savefig(file_name)
    plt.clf()

    plt.plot(theta_values, recall_values)
    plt.xlabel('theta')
    plt.ylabel('recall')
    file_name = location + "theta_v_recall.png"
    plt.savefig(file_name)
    plt.clf()

    plt.plot(theta_values, f1_values)
    plt.xlabel('theta')
    plt.ylabel('f1_score')
    file_name = location + "theta_v_f1Score.png"
    plt.savefig(file_name)
    plt.clf()

    plt.plot(recall_values, precision_values)
    plt.xlabel('recall')
    plt.ylabel('precision')
    file_name = location + "precision_v_recall.png"
    plt.savefig(file_name)
    plt.clf()
