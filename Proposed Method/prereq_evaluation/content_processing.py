import pandas as pd


def merge_ground_tfidf(df_ground, df_tfidf):
	for i in range(df_ground.shape[0]):
		topic_a = df_ground[["topic_a"]].iloc[i].values[0]
		topic_b = df_ground[["topic_b"]].iloc[i].values[0]
		df_ground.at[i, "tfidf_score"] = df_tfidf.at[topic_a, topic_b]
	return df_ground


def main_function(groud_truth_file, tfidf_score_file):
	df_ground = pd.read_csv(groud_truth_file)
	df_tfidf = pd.read_csv(tfidf_score_file)
	df_tfidf.set_index("concept", inplace = True)

	df_merge = merge_ground_tfidf(df_ground, df_tfidf)
	return df_merge

groud_truth_file = "../output_files/physics_labeled_pairs.csv"
tfidf_score_file = "../concept_prereqs/data/match_prereq_pairs_matrix.csv"

df_final = main_function(groud_truth_file, tfidf_score_file)
df_final.to_csv("data/final_prereq_file.csv")