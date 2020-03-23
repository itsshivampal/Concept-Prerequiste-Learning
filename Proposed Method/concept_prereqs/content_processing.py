import pandas as pd
import collections


def merge_files(concept_data_file, concept_rank_file):
	df1 = pd.read_csv(concept_data_file)
	df2 = pd.read_csv(concept_rank_file)

	for i in range(df1.shape[0]):
		concept1 = df1[["concept"]].iloc[i].values[0]
		for j in range(df2.shape[0]):
			concept2 = df2[["concept"]].iloc[j].values[0]
			if concept1 == concept2:
				break
		df1.at[i, "rank"] = df2[["rank"]].iloc[j].values[0]
		df1.at[i, "rank_pos"] = df2[["concept_pos"]].iloc[j].values[0]

	final_df = df1[["type", "concept", "rank", "single_score", "single_index", "first_index", "rank_pos"]]
	final_df = final_df.rename(columns = {"single_score": "score", "single_index": "match_index"})
	return final_df


def read_book_data(file_name):
    df = pd.read_csv(file_name, encoding = "utf-8")
    all_data = {}
    for i in range(df.shape[0]):
        if df[["tagged_content"]].iloc[i].isna().values[0]:
            content = ""
        else:
            content = df[["tagged_content"]].iloc[i].values[0]
        all_data[i] = {
            "section": df[["section"]].iloc[i].values[0],
            "title": df[["title"]].iloc[i].values[0],
            "content": content
        }
    return all_data



def get_section_data(book_data):
    section_list = [book_data[i]["section"] for i in range(len(book_data))]
    section_data = {}
    for i in range(len(section_list)):
        current_collection = [section_list[i]]
        flag = 0
        for j in range(i+1, len(section_list)):
            x1 = len(section_list[i].split("."))
            x2 = len(section_list[j].split("."))
            if x2 > x1:
                current_collection.append(section_list[j])
            else:
                section = section_list[i]
                section_data[section] = "|".join(current_collection)
                flag = 1
                break
        if flag == 0:
            section = section_list[i]
            section_data[section] = "|".join(current_collection)
    return section_data


#------------------------------------------------------------------------------------------------


def get_data(book_data, section):
    for i in range(len(book_data)):
        if book_data[i]["section"] == section:
            break
    title = str(book_data[i]["title"])
    content = str(book_data[i]["content"])
    text = title + "\n" + content
    return text


def get_section_content(section, section_data, book_data):
    req_sections = section_data[section].split("|")
    content = ""
    for section in req_sections:
        content += get_data(book_data, section) + "\n"
    return content

def get_complete_section_data(sections, section_data, book_data):
	print(sections)
	sections = sections.split("|")
	content = ""
	for section in sections:
		content += get_section_content(section, section_data, book_data) + "\n"
	return content


#------------------------------------------------------------------------------------------------


def get_concept_from_content(content):
	concepts = []
	c1 = content.split("<b>")
	for j in range(1, len(c1)):
		concept = c1[j].split("</b>")[0]
		concepts.append(concept)
	return concepts



def concepts_collections(concepts):
	counter = collections.Counter(concepts)
	concept_list = list(counter.keys())
	freq_list = list(counter.values())
	concept_list = "|".join(concept_list)
	freq_list = [str(freq) for freq in freq_list]
	freq_list = "|".join(freq_list)
	return (concept_list, freq_list)



#------------------------------------------------------------------------------------------------




def main_function(df_concept_data, book_data_file):
	book_data = read_book_data(book_data_file)
	section_data = get_section_data(book_data)

	for i in range(df_concept_data.shape[0]):
		if df_concept_data[["type"]].iloc[i].values[0] != 0:
			match_index = df_concept_data[["match_index"]].iloc[i].values[0]
			first_index = df_concept_data[["first_index"]].iloc[i].values[0]

			match_content = get_complete_section_data(match_index, section_data, book_data)
			first_content = get_complete_section_data(first_index, section_data, book_data)

			match_concepts = get_concept_from_content(match_content)
			match_concept_list, match_freq_list = concepts_collections(match_concepts)

			first_concepts = get_concept_from_content(first_content)
			first_concept_list, first_freq_list = concepts_collections(first_concepts)
		else:
			match_concept_list = ""
			match_freq_list = ""
			first_concept_list = ""
			first_freq_list = ""

		df_concept_data.at[i, "match_concept_list"] = match_concept_list
		df_concept_data.at[i, "match_freq_list"] = match_freq_list
		df_concept_data.at[i, "first_concept_list"] = first_concept_list
		df_concept_data.at[i, "first_freq_list"] = first_freq_list

	return df_concept_data


concept_data_file = "../output_files/concept_final_indexing.csv"
concept_rank_file = "../output_files/concept_ranking.csv"
book_data_file = "../output_files/physics_normalized_content.csv"

df_concept_data = merge_files(concept_data_file, concept_rank_file)


df = main_function(df_concept_data, book_data_file)

df.to_csv("data/concept_all_data.csv")

final_df = df[["type", "concept", "rank", "score", "match_concept_list", "match_freq_list", "first_concept_list", "first_freq_list"]]
final_df.to_csv("data/req_concept_data.csv")


