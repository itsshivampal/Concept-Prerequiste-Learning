import pandas as pd


def get_prereq_pairs(df):
	concept_list = list(df["concept"])
	df.set_index("concept", inplace = True)
	prereq_pairs = {
		"topic_a": [],
		"topic_b": [],
		"score": []
	}
	for concept1 in concept_list:
		for concept2 in concept_list:
			tfidf_score = float(df.at[concept1, concept2])
			if tfidf_score > 0.0:
				prereq_pairs["topic_a"].append(concept1)
				prereq_pairs["topic_b"].append(concept2)
				prereq_pairs["score"].append(tfidf_score)
	return prereq_pairs, concept_list


def sort_all_pairs(new_pairs, all_pairs):
	df = pd.DataFrame(columns = ["topic_a", "topic_b", "score"])
	for i in range(len(all_pairs)):
		df = df.append(all_pairs[i], ignore_index = True)
	for i in range(len(new_pairs)):
		df = df.append(new_pairs[i], ignore_index = True)
	df = df.sort_values(by = ["score"])
	df.drop_duplicates(subset = ["topic_a", "topic_b"], keep = "last", inplace = True)
	all_data = {}
	for i in range(df.shape[0]):
		all_data[i] = {
			"topic_a": df[["topic_a"]].iloc[i].values[0],
			"topic_b": df[["topic_b"]].iloc[i].values[0],
			"score": df[["score"]].iloc[i].values[0]
		}
	return all_data


def check_relevant_pairs(all_pairs, pair):
	topic_b = pair["topic_b"]
	new_pairs = {}
	index = 0
	for i in range(len(all_pairs)):
		if topic_b == all_pairs[i]["topic_a"]:
			new_pairs[index] = {
				"topic_a": pair["topic_a"],
				"topic_b": all_pairs[i]["topic_b"],
				"score": float(pair["score"])*float(all_pairs[i]["score"])
			}
			index += 1
	pairs_len = len(all_pairs)
	all_pairs[pairs_len] = pair
	all_pairs = sort_all_pairs(new_pairs, all_pairs)
	return all_pairs



def get_all_pairs(prereq_pairs):
	all_pairs = {}
	all_pairs[0] = {
		"topic_a": prereq_pairs["topic_a"][0],
		"topic_b": prereq_pairs["topic_b"][0],
		"score": prereq_pairs["score"][0]
	}
	for i in range(1, len(prereq_pairs["topic_a"])):
	# for i in range(1, 31):
		print(i)
		pair = {
			"topic_a": prereq_pairs["topic_a"][i],
			"topic_b": prereq_pairs["topic_b"][i],
			"score": prereq_pairs["score"][i]
		}
		all_pairs = check_relevant_pairs(all_pairs, pair)
	df = pd.DataFrame(columns = ["topic_a", "topic_b", "score"])
	for i in range(len(all_pairs)):
		df = df.append(all_pairs[i], ignore_index = True)
	return df


def get_null_matrix(concept_list):
	data = {"concept": concept_list}
	for concept in concept_list:
		data[concept] = [0.0 for i in range(len(concept_list))]
	df = pd.DataFrame(data)
	df.set_index("concept", inplace = True)
	return df



def get_prereq_matrix(df, concept_list):
	df_matrix = get_null_matrix(concept_list)
	for i in range(df.shape[0]):
		topic_a = df[["topic_a"]].iloc[i].values[0]
		topic_b = df[["topic_b"]].iloc[i].values[0]
		score = df[["score"]].iloc[i].values[0]
		df_matrix.at[topic_a, topic_b] = float(score)
	return df_matrix


def book_name_correction(concept_list, df):
	for concept in concept_list:
		df.at[concept, "Physics"] = 1.0
	for concept in concept_list:
		df.at["Physics", concept] = 0.0
	return df


def get_all_prereq_pairs(df_match):
	# df_match = pd.read_csv(first_prereq_file)
	match_prereq_pairs, concept_list = get_prereq_pairs(df_match)
	df_match_all_pairs = get_all_pairs(match_prereq_pairs)
	df_prereq_matrix = get_prereq_matrix(df_match_all_pairs, concept_list)

	df = book_name_correction(concept_list, df_prereq_matrix)
	return df
