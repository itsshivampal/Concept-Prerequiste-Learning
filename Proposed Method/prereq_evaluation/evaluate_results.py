import pandas as pd
import matplotlib.pyplot as plt


def check_state(val, theta):
    if val >= theta: return 1
    else: return 0


def compare_result(result, truth):
    if truth == 1:
        if result == 1: return 1
        elif result == 0: return 2
    elif truth == 0:
        if result == 1: return 3
        elif result == 0: return 4




def estimation_measures(TP, FN, FP, TN):
    if TP == 0 and FP == 0:
        precision = 0
    else:
        precision = TP/(TP + FP)

    if TP == 0 and FN == 0:
        recall = 0
    else:
        recall = TP/(TP + FN)

    accuracy = (TP + TN)/(TP + FN + FP + TN)
    if precision == 0 and recall == 0:
        f1_score = 0
    else:
        f1_score = 2*precision*recall/(precision + recall)
    data = {
        "precision": precision,
        "recall": recall,
        "accuracy": accuracy,
        "f1_score": f1_score
    }
    return data



def check_estimation(y_estimate, y_truth, theta):
    TP = 0
    TN = 0
    FN = 0
    FP = 0
    for i in range(y_estimate.shape[0]):
        estimated = y_estimate.iloc[i].values[0]
        truth = y_truth.iloc[i].values[0]
        result = check_state(estimated, theta)
        score_state = compare_result(result, truth)
        if score_state == 1: TP += 1
        elif score_state == 2: FN += 1
        elif score_state == 3: FP += 1
        elif score_state == 4: TN += 1
    print(TP, FN, FP, TN)
    data = estimation_measures(TP, FN, FP, TN)
    return data


def check_accuracy_measures(file_name, theta):
    df = pd.read_csv(file_name, encoding = "utf-8")
    y_tfidf = df[["tfidf_score"]]
    y_truth = df[["relation"]]
    data = check_estimation(y_tfidf, y_truth, theta)
    return data



def plots_checking(theta_values, accuracy_values, precision_values, recall_values, f1_values):
    location = "data/"

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



def main_function(prereq_file):
    theta_values = [float("{0:.2f}".format((0.0 + 0.02*i))) for i in range(50)]
    accuracy_values = []
    precision_values = []
    recall_values = []
    f1_values = []
    
    for theta in theta_values:
        estimated_results = check_accuracy_measures(prereq_file, theta)
        accuracy_values.append(estimated_results["accuracy"])
        precision_values.append(estimated_results["precision"])
        recall_values.append(estimated_results["recall"])
        f1_values.append(estimated_results["f1_score"])
        print(theta, estimated_results)
    plots_checking(theta_values, accuracy_values, precision_values, recall_values, f1_values)


prereq_file = "data/final_prereq_file.csv"

main_function(prereq_file)
