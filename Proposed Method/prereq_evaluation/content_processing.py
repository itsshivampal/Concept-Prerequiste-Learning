import pandas as pd


def merge_ground_tfidf(df_ground, df_tfidf, df_wiki_tfidf):
	for i in range(df_ground.shape[0]):
		topic_a = df_ground[["topic_a"]].iloc[i].values[0]
		topic_b = df_ground[["topic_b"]].iloc[i].values[0]
		df_ground.at[i, "tfidf_score"] = df_tfidf.at[topic_a, topic_b]

		wiki_tfidf_val = float(df_wiki_tfidf.at[topic_a, topic_b])

		if wiki_tfidf_val != 0.0:
			df_ground.at[i, "wiki_tfidf_score"] = float(df_tfidf.at[topic_a, topic_b])
		else:
			df_ground.at[i, "wiki_tfidf_score"] = 0.0

	return df_ground


def main_function(groud_truth_file, tfidf_score_file, wiki_tfidf):
	df_ground = pd.read_csv(groud_truth_file)
	df_tfidf = pd.read_csv(tfidf_score_file)
	df_tfidf.set_index("concept", inplace = True)

	df_wiki_tfidf = pd.read_csv(wiki_tfidf)
	df_wiki_tfidf.set_index("concept", inplace = True)

	df_merge = merge_ground_tfidf(df_ground, df_tfidf, df_wiki_tfidf)
	return df_merge

groud_truth_file = "../output_files/physics_labeled_pairs.csv"
tfidf_score_file = "../concept_prereqs/data/match_prereq_pairs_matrix.csv"
wiki_tfidf_score_file = "../output_files/wiki_tfidf_matrix.csv"


df_estimated = main_function(groud_truth_file, tfidf_score_file, wiki_tfidf_score_file)
df_estimated.to_csv("../output_files/proposed_estimated_results.csv")