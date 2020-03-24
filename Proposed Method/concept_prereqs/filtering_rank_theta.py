import pandas as pd


def theta_filtering(theta, df):
	for i in range(df.shape[0]):
		score = float(df[["score"]].iloc[i].values[0])
		if theta > score:
			df.at[i, "theta_match_concepts"] = ""
			df.at[i, "theta_match_freq"] = ""
			df.at[i, "theta_first_concepts"] = ""
			df.at[i, "theta_first_freq"] = ""
		else:
			df.at[i, "theta_match_concepts"] = df[["match_concept_list"]].iloc[i].values[0]
			df.at[i, "theta_match_freq"] = df[["match_freq_list"]].iloc[i].values[0]
			df.at[i, "theta_first_concepts"] = df[["first_concept_list"]].iloc[i].values[0]
			df.at[i, "theta_first_freq"] = df[["first_freq_list"]].iloc[i].values[0]
	return df

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
	df.reset_index(drop=True,inplace=True)
	# concept_list = list(df["concept"])
	concept_list = []
	current_rank = 0
	for i in range(df.shape[0]):
		current_rank = df[["rank"]].iloc[i].values[0]
		concept_list = [df[["concept"]].iloc[j].values[0] for j in range(i) if df[["rank"]].iloc[j].values[0] < current_rank]

		# concept_list.append(df[["concept"]].iloc[i].values[0])

		if df[["theta_match_concepts"]].iloc[i].isna().values[0]:
			rank_match_concepts = ""
			rank_match_freq = ""
		else:
			match_concepts = df[["theta_match_concepts"]].iloc[i].values[0]
			match_freq = df[["theta_match_freq"]].iloc[i].values[0]
			rank_match_concepts, rank_match_freq = remove_concepts(i, concept_list, match_concepts, match_freq)

		if df[["theta_first_concepts"]].iloc[i].isna().values[0]:
			rank_first_concepts = ""
			rank_first_freq = ""
		else:			
			first_concepts = df[["theta_first_concepts"]].iloc[i].values[0]
			first_freq = df[["theta_first_freq"]].iloc[i].values[0]
			rank_first_concepts, rank_first_freq = remove_concepts(i, concept_list, first_concepts, first_freq)

		df.at[i, "rank_match_concepts"] = rank_match_concepts
		df.at[i, "rank_match_freq"] = rank_match_freq
		df.at[i, "rank_first_concepts"] = rank_first_concepts
		df.at[i, "rank_first_freq"] = rank_first_freq

	return df



def main_function(concept_content_file, theta):
	df = pd.read_csv(concept_content_file)
	df = theta_filtering(theta, df)
	df = rank_filtering(df)
	return df


concept_content_file = "data/req_concept_data.csv"
theta = 0.12

df = main_function(concept_content_file, theta)

output_file1 = "data/all_theta_rank_filter.csv"
output_file2 = "data/req_theta_rank_filter.csv"

df.to_csv(output_file1)

final_df = df[["concept", "rank", "rank_match_concepts", "rank_match_freq", "rank_first_concepts", "rank_first_freq"]]
final_df.to_csv(output_file2)


