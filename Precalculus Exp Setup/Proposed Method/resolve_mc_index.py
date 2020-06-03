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



def save_concept_resolve_data(data):
	columns = ["concept", "type", "index", "hr_index", "book1", "book2", "book3"]
	df = pd.DataFrame(columns = columns)
	for i in range(len(data)):
		df = df.append(data[i], ignore_index = True)
	return df



def read_hr_index(df):
    data = {}
    for i in range(df.shape[0]):
        concept = df[["concept"]].iloc[i].values[0]
        if df[["index"]].iloc[i].isna().values[0]:
            index = []
            hr_index = []
        else:
            index = df[["index"]].iloc[i].values[0].split("|")
            hr_index = df[["hr_index"]].iloc[i].values[0].split("|")
        data[i] = {
            "concept" : concept,
            "type" : df[["type"]].iloc[i].values[0],
            "index" : index,
            "hr_index": hr_index
        }
    return data


#--------------------------------------------------------------


def text_cleaning(text):
	tokens = nltk.word_tokenize(text)
	return tokens


def tfidf_document_similarity(documents):
	tfidf_vectorizer = TfidfVectorizer(tokenizer = text_cleaning)
	tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
	doc_similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
	return doc_similarity


def get_subsets(arr):
	subsets = []
	for l in range(0, len(arr) + 1):
		for subset in itertools.combinations(arr, l):
			subsets.append(subset)
	subsets = [subsets[i] for i in range(1, len(subsets))]
	return subsets


def get_section_combination(arr, chapter_distribution):
	book1 = []
	book2 = []
	book3 = []
	for section in arr:
		chpt_num = int(section.split(".")[0])
		if chpt_num in chapter_distribution[0]:
			book1.append(section)
		elif chpt_num in chapter_distribution[1]:
			book2.append(section)
		elif chpt_num in chapter_distribution[2]:
			book3.append(section)

	final_book_sections = []
	if len(book1) > 0:
		subset1 = get_subsets(book1)
		final_book_sections.append(subset1)
	else: final_book_sections.append([])

	if len(book2) > 0:
		subset2 = get_subsets(book2)
		final_book_sections.append(subset2)
	else: final_book_sections.append([])

	if len(book3) > 0:
		subset3 = get_subsets(book3)
		final_book_sections.append(subset3)
	else: final_book_sections.append([])

	return final_book_sections

def get_final_section_list(documents, final_book_sections, concept, wikipedia_data_file):
	wiki_summary, wiki_content = get_wiki_data(concept, wikipedia_data_file)
	wiki_content = clean_text(wiki_content)
	final_section = []
	for section_combination in final_book_sections:
		if len(section_combination) == 0:
			final_section.append([])
		elif len(section_combination) == 1:
			final_section.append(section_combination[0])
		else:
			all_documents = [wiki_content]
			for sections in section_combination:
				content = ""
				for section in sections:
					content += documents[section]["content"] + "\n"
				all_documents.append(content)
			score = tfidf_document_similarity(all_documents)[0]
			max_score = score[1]
			index = 1
			for i in range(1, len(score)):
				if score[i] > max_score:
					max_score = score[i]
					index = i
			best_section = section_combination[index-1]
			final_section.append([best_section[0]])
	return final_section



def resolve_multi_sections(sections, concept, chapter_distribution, wikipedia_data_file, book_content_file):
	resulted_sections = []
	documents = {}
	for section in sections:
		documents[section] = {
			"content": clean_text(get_book_data(section, book_content_file))
		}
	section_combination = get_section_combination(sections, chapter_distribution)
	resulted_sections = get_final_section_list(documents, section_combination, concept, wikipedia_data_file)
	return resulted_sections



def best_section_for_concept(sections):
	pass





def sort_mc_sections(df, chapter_distribution, wikipedia_data_file, book_content_file):
	title_match_data = read_hr_index(df)
	all_data = {}
	for i in range(len(title_match_data)):
	# for i in range(10):
		func_type = int(title_match_data[i]["type"])
		concept = title_match_data[i]["concept"]
		sections = title_match_data[i]["index"]
		hr_index = title_match_data[i]["hr_index"]
		if func_type != 0:
			mc_index = resolve_multi_sections(hr_index, concept, chapter_distribution, wikipedia_data_file, book_content_file)
			book1 = "|".join(mc_index[0])
			book2 = "|".join(mc_index[1])
			book3 = "|".join(mc_index[2])
		else:
			book1 = ""
			book2 = ""
			book3 = ""
		all_data[i] = {
			"concept": concept,
			"type": func_type,
			"index" : "|".join(sections),
			"hr_index": "|".join(hr_index),
			"book1": book1,
			"book2": book2,
			"book3": book3,
		}
	df = save_concept_resolve_data(all_data)
	return df
