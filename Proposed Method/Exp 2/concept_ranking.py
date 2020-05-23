import pandas as pd


def get_final_ranking(df_book, df_concept):
	section_list = list(df_book)
	current_rank = 1
	for section in section_list:
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
    df = df_concept_rank[["concept", "type", "rank"]]
    # df = df.sort_values(by = ["rank"])
    return df
