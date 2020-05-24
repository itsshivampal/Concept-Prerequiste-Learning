import pandas as pd
import numpy as np


def get_section_data(section_list):
    section_data = {}
    for i in range(len(section_list)):
        current_collection = []
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


def find_index(lst, elem, pos):
    index = lst.index(elem)
    return index + pos


def previous_elem(b):
    split_b = b.split(".")
    b = [int(elem) for elem in split_b]
    b[-1] = b[-1] - 1
    b = [str(i) for i in b]
    return ".".join(b)


def insert_element(elem, lst):
    elem_parent = elem[:-2]
    last_text = elem[-1]
    if last_text == "1":
        index = find_index(lst, elem_parent, 1)
    else:
        flag = True
        current_elem = elem
        while flag:
            req_elem = previous_elem(current_elem)
            if req_elem in lst:
                flag = False
            else:
                current_elem = req_elem
        index = find_index(lst, req_elem, 0)
    lst.insert(index, elem)
    return lst


def get_section_ranking(section, section_data):
	last_chpt = int(section[-1].split(".")[0])
	final_ranking = []
	for chpt in range(1, last_chpt + 1):
	    chapter_ranking = []
	    chapter_ranking.append(str(chpt))
	    chpt_list = section_data[str(chpt)].split("|")
	    if chpt_list[0] == '':
	        pass
	    else:
	        for sect in chpt_list:
	            chapter_ranking = insert_element(sect, chapter_ranking)
	    chapter_ranking.reverse()
	    for sect in chapter_ranking:
	        final_ranking.append(sect)
	return final_ranking

#-----------------------------------------------------------------------------

def get_final_ranking(df_book, df_concept):
	section_list = list(df_book)
	section_data = get_section_data(section_list)
	section_ranking = get_section_ranking(section_list, section_data)
	current_rank = 1
	for section in section_ranking:
		flag = 0
		for i in range(df_concept.shape[0]):
			current_pos = df_concept[["concept_pos"]].iloc[i].values[0]
			if current_pos == section:
				df_concept.at[i, "rank"] = current_rank
				flag = 1
		if flag:
			current_rank += 1
	return df_concept



def get_final_index(df):
    concept_sections = df[["book1_fo", "book2_fo", "book3_fo"]].values
    final_sections = []
    for concept_data in concept_sections:
        sections = [concept_data[j] for j in range(3) if concept_data[j] == concept_data[j]]
        final_sections.append(sections[0])
    df["concept_pos"] = final_sections
    return df



def get_concept_ranking(concept_index, book_file):
    df_book = pd.read_csv(book_file)["section"]
    df_concept_index = get_final_index(concept_index)
    df_concept_rank = get_final_ranking(df_book, df_concept_index)
    df = df_concept_rank[["concept", "type", "rank", "concept_pos"]]
    # df = df.sort_values(by = ["rank"])
    return df
