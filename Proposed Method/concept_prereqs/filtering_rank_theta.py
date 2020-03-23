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
			df.at[i, "theta_first_freq"] = df[["first_concept_list"]].iloc[i].values[0]
	return df

def remove_concepts(concept_list, concept_collections, frequency_collections):
	final_concept_collections = []
	final_frequency_collections = []
	for i in range(len(concept_list)):
		concepts = concept_collections[i].split("|")
		frequency = frequency_collections[i].split("|")
		final_concepts = []
		final_frequency = []
		for j in range(len(concepts)):
			for k in range(i):
				if concepts[j] == concept_list[k]:
					final_concepts.append(concepts[j])
					final_frequency.append(frequency[j])
					break
		final_concepts = final_concepts.join("|")
		final_frequency = final_frequency.join("|")
		final_concept_collections.append(final_concepts)




def rank_filtering(df):
	df = df.sort_values(by = ['rank'])
	concept_list = list(df["concept"])

	#remove from theta_match_concepts
	match_concepts = list(df["theta_match_concepts"])
	match_freq = list(df["theta_match_freq"])
	rank_match_concepts, rank_match_freq = remove_concepts(concept_list, match_concepts, match_freq)



def main_function(concept_content_file, theta):
	df = pd.read_csv(concept_content_file)
	df = theta_filtering(theta, df)
	df = rank_filtering(df)
	return df


concept_content_file = "data/req_concept_data.csv"
theta = 0.12