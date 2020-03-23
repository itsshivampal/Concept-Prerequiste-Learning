import pandas as pd


def get_final_ranking(df_book, df_concept):
	section_list = list(df_book)
	current_rank = 1
	for section in section_list:
		flag = 0
		for i in range(df_concept.shape[0]):
			current_pos = df_concept[["concept_pos"]].iloc[i].values[0]
			if current_pos == section:
				df_concept.at[i, "rank"] = current_rank
				flag = 1
		if flag:
			current_rank += 1
	return df_concept



def get_final_index(df, theta):
	match_score = list(df["content_concept_score"])
	match_score = [float(score) for score in match_score]
	for i in range(df.shape[0]):
		if match_score[i] < theta:
			if df[["single_content_match"]].iloc[i].isna().values[0]:
				final_index = df[["single_title_match"]].iloc[i].values[0]
			else:
				final_index = df[["single_content_match"]].iloc[i].values[0]
		else:
			final_index = df[["single_title_match"]].iloc[i].values[0]
		df.at[i, "concept_pos"] = final_index
	return df



def main_function(concept_index_file, book_file, theta):
	df_book = pd.read_csv(book_file)["section"]
	df_concept_index = pd.read_csv(concept_index_file)
	df_concept_index = get_final_index(df_concept_index, theta)
	df_concept_index = get_final_ranking(df_book, df_concept_index)
	return df_concept_index


concept_index_file = "data/concept_indexing.csv"
book_file = "../output_files/physics_normalized_content.csv"
theta = 0.12
df = main_function(concept_index_file, book_file, theta)

local_output_file = "data/concept_ranking.csv"
df = df.sort_values(by = ["rank"])
df.to_csv(local_output_file)

output_file = "../output_files/concept_ranking.csv"
final_df = df[["concept", "type", "concept_pos", "rank"]]
final_df.to_csv(output_file)


