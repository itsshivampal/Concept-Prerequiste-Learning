import pandas as pd
import collections


def read_concept_data(file_name):
	df = pd.read_csv(file_name, encoding = "utf-8")
	req_data = {}
	for i in range(df.shape[0]):
		concept = df[["concept"]].iloc[i].values[0]
		func_type = df[["type"]].iloc[i].values[0]
		if func_type != 0: title_match_index = df[["index"]].iloc[i].values[0]
		else: title_match_index = ""

		req_data[i] = {
			"concept": concept,
			"type": func_type,
			"title_match_index": title_match_index,
			"content_match_index": [],
			"freq_content_match": []
		}
	return req_data



def read_book_data(file_name):
	df = pd.read_csv(file_name, encoding = "utf-8")
	req_data = {}
	for i in range(df.shape[0]):
		section = df[["section"]].iloc[i].values[0]
		if df[["tagged_content"]].iloc[i].isna().values[0]:
			content = ""
		else:
			content = df[["tagged_content"]].iloc[i].values[0]
		req_data[i] = {
			"section": section,
			"content": content
		}
	return req_data




def get_concept_from_content(data):
	for i in range(len(data)):
		content = data[i]["content"]
		concepts = []

		c1 = content.split("<b>")
		for j in range(1, len(c1)):
			concept = c1[j].split("</b>")[0]
			concepts.append(concept)

		data[i]["concepts"] = concepts
	return data


def concepts_collections(concepts):
	counter = collections.Counter(concepts)
	concept_list = list(counter.keys())
	freq_list = list(counter.values())
	return (concept_list, freq_list)


def get_concept_content_matching(concept_data, book_data):
	for i in range(len(book_data)):
		concepts = book_data[i]["concepts"]
		concept_list, freq_list = concepts_collections(concepts)
		for j in range(len(concept_list)):
			concept = concept_list[j]
			for k in range(len(concept_data)):
				if concept_data[k]["concept"] == concept:
					section = book_data[i]["section"]
					concept_data[k]["content_match_index"].append(section)
					concept_data[k]["freq_content_match"].append(freq_list[j])
	return concept_data


def get_single_content_match(sections, frequency):
	index = 0
	for i in range(len(frequency)):
		if frequency[i] > 1:
			index = i
			break
	if len(sections) > 0: section = sections[index]
	else: section = ""
	return section



def sort_concept_data(concept_data):
	for i in range(len(concept_data)):
		index = concept_data[i]["content_match_index"]
		freq = concept_data[i]["freq_content_match"]

		concept_data[i]["single_title_match"] = concept_data[i]["title_match_index"].split("|")[0]
		concept_data[i]["single_content_match"] = get_single_content_match(index, freq)
		concept_data[i]["content_match_index"] = "|".join(index)
		freq = [str(f) for f in freq]
		concept_data[i]["freq_content_match"] = "|".join(freq)
	return concept_data



def save_concept_data(concept_data, output_file):
	columns = ["concept", "type", "single_title_match", "single_content_match", "title_match_index", "content_match_index", "freq_content_match"]
	df = pd.DataFrame(columns = columns)
	for i in range(len(concept_data)):
		df = df.append(concept_data[i], ignore_index = True)
	df.to_csv(output_file)
	return True



def main_function(book_data_file, concept_data_file, output_file):
	book_data = read_book_data(book_data_file)
	concept_data = read_concept_data(concept_data_file)
	book_data = get_concept_from_content(book_data)
	concept_data = get_concept_content_matching(concept_data, book_data)
	concept_data = sort_concept_data(concept_data)
	save_concept_data(concept_data, output_file)
	return True





book_data_file = "../output_files/physics_normalized_content.csv"
concept_data_file = "../output_files/concept_final_indexing.csv"
output_file = "data/concept_indexing.csv"
main_function(book_data_file, concept_data_file, output_file)

