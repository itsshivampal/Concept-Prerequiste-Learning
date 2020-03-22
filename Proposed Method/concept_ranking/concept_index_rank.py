import pandas as pd



def get_final_ranking(df_book, df_concept_index):
	pass


def get_final_index(df):
	pass



def main_function(concept_index_file, book_file, output_file):
	df_book = pd.read_csv(book_file)["section"]
	df_concept_index = pd.read_csv(concept_index_file)
	df_concept_index = get_final_index(df_concept_index)		
	df_concept_index = get_final_ranking(df_book, df_concept_index)
	df_concept_index.to_csv(output_file)


concept_index_file = "data/concept_indexing.csv"
book_file = "../output_files/physics_normalized_content.csv"
output_file = "../output_files/concept_ranking.csv"