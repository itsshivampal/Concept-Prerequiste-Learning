import pandas as pd
import math


def read_data(df):
	concept_list = [df[["concept"]].iloc[i].values[0] for i in range(df.shape[0])]
	match_data = {}
	first_data = {}
	for i in range(df.shape[0]):
		concept = df[["concept"]].iloc[i].values[0]
		if df[["rank_match_concepts"]].iloc[i].isna().values[0]:
			match_concepts = ""
			match_freq = ""
		else:
			match_concepts = df[["rank_match_concepts"]].iloc[i].values[0].split("|")
			match_freq = df[["rank_match_freq"]].iloc[i].values[0].split("|")
		match_data[concept] = {
			"concept": match_concepts,
			"freq": match_freq
		}

		if df[["rank_first_concepts"]].iloc[i].isna().values[0]:
			first_concepts = ""
			first_freq = ""
		else:			
			first_concepts = df[["rank_first_concepts"]].iloc[i].values[0].split("|")
			first_freq = df[["rank_first_freq"]].iloc[i].values[0].split("|")
		first_data[concept] = {
			"concept": first_concepts,
			"freq": first_freq
		}
	return concept_list, match_data, first_data


def get_null_matrix(concept_list):
	data = {"concept": concept_list}
	for concept in concept_list:
		data[concept] = [0.0 for i in range(len(concept_list))]
	df = pd.DataFrame(data)
	df.set_index("concept", inplace = True)
	return df


def get_tf_matrix(concept_list, term_data):
	df = get_null_matrix(concept_list)
	for concept1 in concept_list:
		concepts = term_data[concept1]["concept"]
		frequency = term_data[concept1]["freq"]
		freq_sum = 0
		for freq in frequency:
			freq_sum = freq_sum + int(freq)
		for i in range(len(concepts)):
			term = concepts[i]
			freq = frequency[i]
			# print(float(freq)/float(freq_sum))
			df.at[concept1, term] = float(freq)/float(freq_sum)
	return df


def get_term_idf(concept_list, df):
	idf_data = {}
	for concept in concept_list:
		freq_list = list(df[concept])
		count = 0
		for val in freq_list:
			if val != 0: count += 1
		N = len(freq_list)
		idf_val = math.log(N/(count + 1))
		idf_data[concept] = idf_val
	return idf_data


def get_tf_idf_matrix(concept_list, df, idf_data):
	for concept1 in concept_list:
		for concept2 in concept_list:
			tf = df.loc[concept2, concept1]
			idf = idf_data[concept1]
			tf_idf = tf*idf
			df.at[concept2, concept1] = tf_idf
	return df



def main_function(concept_prereq_file):
	df = pd.read_csv(concept_prereq_file)
	concept_list, match_data, first_data = read_data(df)

	df_match = get_tf_matrix(concept_list, match_data)
	match_idf_data = get_term_idf(concept_list, df_match)
	df_math_tfidf =get_tf_idf_matrix(concept_list, df_match, match_idf_data)
	df_math_tfidf.to_csv("data/match_tfidf_matrix.csv")

	df_first = get_tf_matrix(concept_list, first_data)
	first_idf_data = get_term_idf(concept_list, df_first)
	df_first_tfidf =get_tf_idf_matrix(concept_list, df_first, first_idf_data)
	df_first_tfidf.to_csv("data/tf_first_matrix.csv")



concept_prereq_file = "data/req_theta_rank_filter.csv"
output_file1 = "data/match_tfidf_matrix.csv"
output_file2 = "data/first_tfidf_matrix.csv"
main_function(concept_prereq_file)


