import pandas as pd
import math


def read_data(df):
	concepts = list(df[["concept"]].values[:,0])
	concept_list = list(df[["filter_concept_list"]].values[:,0])
	freq_list = list(df[["filter_freq_list"]].values[:,0])

	match_data = {}

	for i in range(len(concepts)):
		if concept_list[i] == concept_list[i]: c_list = concept_list[i].split("|")
		else: c_list = ""

		if freq_list[i] == freq_list[i]: f_list = freq_list[i].split("|")
		else: f_list = ""

		match_data[concepts[i]] = {
			"concept": c_list,
			"freq": f_list
		}
	return concepts, match_data


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



def book_name_correction(concept_list, df):
	for concept in concept_list:
		df.at[concept, "Geometry"] = 1.0
	for concept in concept_list:
		df.at["Geometry", concept] = 0.0
	return df


def get_tfidf_score(df):
	concept_list, match_data = read_data(df)
	df_match = get_tf_matrix(concept_list, match_data)
	match_idf_data = get_term_idf(concept_list, df_match)
	df_match_tfidf = get_tf_idf_matrix(concept_list, df_match, match_idf_data)
	df_match_tfidf = book_name_correction(concept_list, df_match_tfidf)
	return df_match_tfidf
