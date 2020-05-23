import pandas as pd


def remove_concepts(i, concept_list, concept_collections, frequency_collections):
	concepts = concept_collections.split("|")
	frequency = frequency_collections.split("|")
	final_concepts = []
	final_frequency = []
	for j in range(len(concepts)):
		if concepts[j] in concept_list:
			final_concepts.append(concepts[j])
			final_frequency.append(frequency[j])
	final_concepts = "|".join(final_concepts)
	final_frequency = "|".join(final_frequency)
	return final_concepts, final_frequency




def rank_filtering(df):
	df = df.sort_values(by = ['rank'])
	df.reset_index(drop=True, inplace=True)
	concept_list = []
	current_rank = 0
	for i in range(df.shape[0]):
		current_rank = df[["rank"]].iloc[i].values[0]
		concept_list = [df[["concept"]].iloc[j].values[0] for j in range(i) if df[["rank"]].iloc[j].values[0] < current_rank]
		if df[["concept_list"]].iloc[i].isna().values[0]:
			rank_concepts = ""
			rank_freq = ""
		else:
			match_concepts = df[["concept_list"]].iloc[i].values[0]
			match_freq = df[["freq_list"]].iloc[i].values[0]
			rank_concepts, rank_freq = remove_concepts(i, concept_list, match_concepts, match_freq)
		df.at[i, "filter_concept_list"] = rank_concepts
		df.at[i, "filter_freq_list"] = rank_freq
	return df



def apply_rank_filter(concept_content, concept_ranking):
    df = pd.concat([concept_content, concept_ranking], axis = 1)
    df = df[["concept", "type", "rank", "concept_list", "freq_list"]]
    df = df.loc[:,~df.T.duplicated(keep='first')]
    df = rank_filtering(df)
    final_df = df[["concept", "type", "rank", "filter_concept_list", "filter_freq_list"]]
    return final_df
