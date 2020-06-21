import pandas as pd
import numpy as np

def merge_ground_tfidf(df_ground, df_tfidf, df_wiki_tfidf, concepts):
	index = 0
	df_req = pd.DataFrame(columns = ['topic_a', 'topic_b', 'relation', 'tfidf_score', 'wiki_tfidf_score'])
	
	for i in range(df_ground.shape[0]):
		topic_a = df_ground[["topic_a"]].iloc[i].values[0]
		topic_b = df_ground[["topic_b"]].iloc[i].values[0]
		relation = df_ground[["relation"]].iloc[i].values[0]

		if topic_a in concepts and topic_b in concepts:
			tfidf_score = float(df_tfidf.at[topic_a, topic_b])
			wiki_tfidf_val = float(df_wiki_tfidf.at[topic_a, topic_b])

			if wiki_tfidf_val != 0.0:
				wiki_tfidf_score = float(df_tfidf.at[topic_a, topic_b])
			else:
				wiki_tfidf_score = 0.0

			data = {
				"topic_a": topic_a,
				"topic_b": topic_b,
				"relation": relation,
				"tfidf_score": tfidf_score,
				"wiki_tfidf_score": wiki_tfidf_score
			}

			df_req = df_req.append(data, ignore_index=True)

	return df_req


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
	concepts = list(df_tfidf["concept"].values)
	df_tfidf.set_index("concept", inplace = True)
	df_wiki_tfidf.set_index("concept", inplace = True)
	df_merge = merge_ground_tfidf(df_ground, df_tfidf, df_wiki_tfidf, concepts)

	return df_merge
