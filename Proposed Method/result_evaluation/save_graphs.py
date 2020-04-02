import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score

file1 = "../output_files/proposed_estimated_results.csv"
file2 = "../output_files/refd_estimated_results.csv"

df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

ground_truth = df1["relation"].to_numpy().ravel()
pr_tfidf = df1["tfidf_score"].to_numpy().ravel()
pr_wiki_tfidf = df1["wiki_tfidf_score"].to_numpy().ravel()
rd_tfidf = df2["refd_tfidf"].to_numpy().ravel()
rd_equal = df2["refd_equal"].to_numpy().ravel()





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
    for i in range(len(y_estimate)):
        estimated = y_estimate[i]
        truth = y_truth[i]
        result = check_state(estimated, theta)
        score_state = compare_result(result, truth)
        if score_state == 1: TP += 1
        elif score_state == 2: FN += 1
        elif score_state == 3: FP += 1
        elif score_state == 4: TN += 1
    print(TP, FN, FP, TN)
    data = estimation_measures(TP, FN, FP, TN)
    return data


def get_pr_area(precision, recall):
	n = len(precision)
	area = 0
	for i in range(1, n):
		area += abs(precision[i]*(recall[i] - recall[i-1]))
	return area



def get_precision_recall(ground_val, est_val):
	precision = []
	recall = []
	theta_values = [float("{0:.2f}".format((0.0 + 0.01*i))) for i in range(100)]
	for theta in theta_values:
		data = check_estimation(est_val, ground_val, theta)
		precision.append(data["precision"])
		recall.append(data["recall"])
	area = get_pr_area(precision, recall)
	return precision, recall, area




precision, recall, area = get_precision_recall(ground_truth, pr_tfidf)
print(area)
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.plot(recall, precision)
plt.savefig("curve.png")
