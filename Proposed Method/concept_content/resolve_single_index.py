import pandas as pd
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from load_data import *
from text_cleaning import clean_text
import re
import itertools

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity




def text_cleaning(text):
	tokens = nltk.word_tokenize(text)
	return tokens


def tfidf_document_similarity(documents):
	tfidf_vectorizer = TfidfVectorizer(tokenizer = text_cleaning)
	tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
	doc_similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
	return doc_similarity





# def compare_sections(section, concept):
# 	wiki_summary, wiki_content = get_wiki_data(concept)
# 	wiki_content = clean_text(wiki_content)
# 	documents = [wiki_content]
# 	for index in section:
# 		content = get_book_data(index)
# 		content = clean_text(content)
# 		documents.append(content)
# 	score = tfidf_document_similarity(documents)[0]
# 	max_score = score[1]
# 	index = 1
# 	for i in range(1, len(score)):
# 		if score[i] > max_score:
# 			max_score = score[i]
# 			index = i
# 	best_section = section[index-1]
# 	return best_section



# def resolve_sections(sections, concept):
# 	section_list = merge_section(sections)
# 	resulted_section = []
# 	for section in section_list:
# 		if len(section) == 1:
# 			resulted_section.append(section[0])
# 		else:
# 			resulted_section.append(compare_sections(section, concept))
# 	return resulted_section




# def get_section_combination(arr):
# 	subsets = []
# 	for l in range(0, len(arr) + 1):
# 		for subset in itertools.combinations(arr, l):
# 			subsets.append(subset)
# 	subsets = [subsets[i] for i in range(1, len(subsets))]
# 	return subsets


# def get_final_section_list(documents, section_combination, concept):
# 	wiki_summary, wiki_content = get_wiki_data(concept)
# 	wiki_content = clean_text(wiki_content)
# 	all_documents = [wiki_content]
# 	for sections in section_combination:
# 		content = ""
# 		for section in sections:
# 			content += documents[section]["content"] + "\n"
# 		all_documents.append(content)
# 	score = tfidf_document_similarity(all_documents)[0]
# 	max_score = score[1]
# 	index = 1
# 	for i in range(1, len(score)):
# 		if score[i] > max_score:
# 			max_score = score[i]
# 			index = i
# 	best_section = section_combination[index-1]
# 	return best_section, max_score



# def resolve_multi_sections(sections, concept):
# 	resulted_section = []
# 	documents = {}
# 	for section in sections:
# 		documents[section] = {
# 			"content": clean_text(get_book_data(section))
# 		}
# 	section_combination = get_section_combination(sections)
# 	resulted_section, max_score = get_final_section_list(documents, section_combination, concept)
# 	return resulted_section, max_score




def get_chapter_clusters(sections):
	chapters = [int(x.split(".")[0]) for x in sections]
	chapt_list = list(set(chapters))

	chapters_data = {}
	for chapt in chapt_list:
		chapters_data[chapt] = []

	for x in sections:
		chapt = int(x.split(".")[0])
		chapters_data[chapt].append(x)

	final_chapt_array = [chapters_data[chapt] for chapt in chapters_data]

	return final_chapt_array





def get_best_chapter(mod_sections, concept):
	wiki_summary, wiki_content = get_wiki_data(concept)
	wiki_content = clean_text(wiki_content)
	all_documents = [wiki_content]

	for sections in mod_sections:
		document = ""
		for section in sections:
			document += clean_text(get_book_data(section)) + "\n"
		all_documents.append(document)

	score = tfidf_document_similarity(all_documents)[0]
	max_score = score[1]
	index = 1
	for i in range(1, len(score)):
		if score[i] > max_score:
			max_score = score[i]
			index = i
	best_section = mod_sections[index-1]

	return (best_section, max_score)




def resolve_single_section(sections, concept, score):
	if len(sections) != 1:
		mod_sections = get_chapter_clusters(sections)
		if len(mod_sections) != 1:
			sections, score = get_best_chapter(mod_sections, concept)
	return (sections, score)





def sort_sections(file_name):
	df = pd.read_csv(file_name, encoding = "utf-8")
	for i in range(df.shape[0]):
	# for i in range(5):
		print(i)
		func_type = int(df[["type"]].iloc[i].values[0])
		if func_type != 0:
			concept = df[["concept"]].iloc[i].values[0]
			mc_index = df[["mc_index"]].iloc[i].values[0].split("|")
			mc_score = df[["score"]].iloc[i].values[0]
			single_index, single_score = resolve_single_section(mc_index, concept, mc_score)
			single_index = "|".join(single_index)
		else:
			single_index = ""
			single_score = 0
		df.at[i, "single_index"] = single_index
		df.at[i, "single_score"] = single_score
	return df





file_name = "data/resolve_mc_index.csv"
output_file = "data/resolve_single_index.csv"
final_df = sort_sections(file_name)
final_df.to_csv(output_file)

