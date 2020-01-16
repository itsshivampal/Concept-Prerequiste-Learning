from library.save_data import *
from library.algorithm_evaluation import evaluate_prereq_estimation
from library.prereq_calculation import get_prereq_relations
import pandas as pd


# file1 = "RefD Implementation/output_data/CS_edge.csv"
# file2 = "RefD Implementation/output_data/final_CS_wiki_data.csv"
# get_prereq_relations(0.02, file1, file2, "refd", "equal", "CS")
#
#
# file1 = "RefD Implementation/output_data/MATH_edge.csv"
# file2 = "RefD Implementation/output_data/final_MATH_wiki_data.csv"
# get_prereq_relations(0.02, file1, file2, "refd", "equal", "MATH")

#-------------------------------------------------------------------------------


file1 = "RefD Implementation/output_data/CS_edge.csv"
file2 = "RefD Implementation/output_data/CS_edge_neg.csv"
prereq_file = "RefD Implementation/output_data/calculated_prereq/CS/prereq_refd_equal_2.csv"

df_cs_edge = pd.read_csv(file1, encoding = "utf-8")
df_cs_edge_neg = pd.read_csv(file2, encoding = "utf-8")
df_prereq_match = pd.read_csv(prereq_file, encoding = "utf-8")



print(df_cs_edge.shape[0])
print(df_cs_edge_neg.shape[0])
print(df_prereq_match.shape[0])

print("#------------------------------------------------------------#")

print(evaluate_prereq_estimation(df_cs_edge, df_cs_edge_neg, df_prereq_match))
