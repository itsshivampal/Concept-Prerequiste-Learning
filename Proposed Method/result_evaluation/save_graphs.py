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

precision, recall, _ = precision_recall_curve(ground_truth, pr_tfidf)
average_precision = average_precision_score(ground_truth, pr_tfidf)

plt.xlabel("Recall")
plt.ylabel("Precision")
plt.plot(recall, precision, label='Precision-recall curve of (area = {1:0.2f})'.format(average_precision))
plt.savefig("curve.png")