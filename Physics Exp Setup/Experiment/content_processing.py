import pandas as pd
import collections
import numpy as np


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
    # title = str(book_data[i]["title"])
    content = str(book_data[i]["content"])
    # text = title + "\n" + content
    return content


def get_section_content(section, section_data, book_data):
    req_sections = section_data[section].split("|")
    content = ""
    for section in req_sections:
        content += get_data(book_data, section) + "\n"
    return content

def get_complete_section_data(sections, section_data, book_data):
	print(sections)
	# sections = sections.split("|")
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




def get_concept_content(df_concept_data, book_data_file):
    book_data = read_book_data(book_data_file)
    section_data = get_section_data(book_data)

    concept_sections = df_concept_data[["book1_fs", "book2_fs", "book3_fs"]].values
    final_sections = []
    for concept_data in concept_sections:
        sections = [concept_data[j] for j in range(3) if concept_data[j] == concept_data[j]]
        final_sections.append(sections)

    for i in range(df_concept_data.shape[0]):
        if df_concept_data[["type"]].iloc[i].values[0] != 0:
            section = final_sections[i]
            concept_content = get_complete_section_data(section, section_data, book_data)

            match_concepts = get_concept_from_content(concept_content)
            match_concept_list, match_freq_list = concepts_collections(match_concepts)

        else:
            # section = [final_sections[i][0]]
            # concept_content = get_complete_section_data(section, section_data, book_data)
            #
            # match_concepts = get_concept_from_content(concept_content)
            # match_concept_list, match_freq_list = concepts_collections(match_concepts)
            
            match_concept_list = ""
            match_freq_list = ""

        df_concept_data.at[i, "concept_list"] = match_concept_list
        df_concept_data.at[i, "freq_list"] = match_freq_list

    return df_concept_data[["concept", "type", "concept_list", "freq_list"]]
