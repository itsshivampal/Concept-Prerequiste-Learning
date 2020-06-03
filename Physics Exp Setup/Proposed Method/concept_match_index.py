import pandas as pd
import collections


def read_concept_data(df):
	req_data = {}
	for i in range(df.shape[0]):
		req_data[i] = {
			"concept" : df[["concept"]].iloc[i].values[0],
			"type" : df[["type"]].iloc[i].values[0],
			"book1_title" : df[["book1"]].iloc[i].values[0],
			"book2_title" : df[["book2"]].iloc[i].values[0],
			"book3_title" : df[["book3"]].iloc[i].values[0],
			"content_match_index": [],
			"freq_content_match": [],
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
		concepts = content.split("|")
		# concepts = []
		#
		# c1 = content.split("<b>")
		# for j in range(1, len(c1)):
		# 	concept = c1[j].split("</b>")[0]
		# 	concepts.append(concept)

		data[i]["concepts"] = concepts
	# data = data.
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


def get_book_content_match(sections, frequency, chapter_distribution):
	required_sections = []
	section_distribution = {}
	for i in range(len(chapter_distribution)):
		section = []
		freq = []
		for j in range(len(sections)):
			chapter = int(sections[j].split(".")[0])
			if chapter in chapter_distribution[i]:
				section.append(sections[j])
				freq.append(frequency[j])
		req_section = get_single_content_match(section, freq)
		required_sections.append(req_section)
	return required_sections



def sort_concept_data(concept_data, chapter_distribution):
	for i in range(len(concept_data)):
		index = concept_data[i]["content_match_index"]
		freq = concept_data[i]["freq_content_match"]
		required_sections = get_book_content_match(index, freq, chapter_distribution)
		concept_data[i]["book1_content"] = required_sections[0]
		concept_data[i]["book2_content"] = required_sections[1]
		concept_data[i]["book3_content"] = required_sections[2]
	return concept_data



def save_concept_data(concept_data):
	columns = ["concept", "type", "book1_title", "book1_content", "book2_title", "book2_content", "book3_title", "book3_content"]
	df = pd.DataFrame(columns = columns)
	for i in range(len(concept_data)):
		df = df.append(concept_data[i], ignore_index = True)
	df1 = df[columns]
	df1 = df1.sort_values(by=['type'])
	return df1



def get_index_from_content(book_data_file, concept_data_file, chapter_distribution):
	book_data = read_book_data(book_data_file)
	concept_data = read_concept_data(concept_data_file)
	book_data = get_concept_from_content(book_data)
	concept_data = get_concept_content_matching(concept_data, book_data)
	concept_data = sort_concept_data(concept_data, chapter_distribution)
	df = save_concept_data(concept_data)
	return df
