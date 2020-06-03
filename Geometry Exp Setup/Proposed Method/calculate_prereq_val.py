import pandas as pd
import numpy as np

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


# def merge_ground_tfidf(df_ground, df_tfidf, df_wiki_tfidf):
# 	for i in range(df_ground.shape[0]):
# 		topic_a = df_ground[["topic_a"]].iloc[i].values[0]
# 		topic_b = df_ground[["topic_b"]].iloc[i].values[0]
#
# 		pred_tfidf_val = float(df_tfidf.at[topic_a, topic_b])
# 		wiki_tfidf_val = float(df_wiki_tfidf.at[topic_a, topic_b])
#
# 		df_ground.at[i, "tfidf_score"] = pred_tfidf_val
# 		df_ground.at[i, "wiki_tfidf_score"] = wiki_tfidf_val
# 	return df_ground


def get_labeled_prereq_val(df_ground, df_tfidf, df_wiki_tfidf):
	df_tfidf.set_index("concept", inplace = True)
	df_wiki_tfidf.set_index("concept", inplace = True)
	df_merge = merge_ground_tfidf(df_ground, df_tfidf, df_wiki_tfidf)

	return df_merge
