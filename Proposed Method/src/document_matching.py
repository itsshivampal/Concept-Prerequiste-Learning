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



def save_concept_resolve_data(data, output_file):
	columns = ["concept", "type", "index", "hr_index", "mc_index", "score"]
	df = pd.DataFrame(columns = columns)
	for i in range(len(data)):
		df = df.append(data[i], ignore_index = True)
	df.to_csv(output_file)
	return True


# Get data from csv files

def is_subsection(s1, s2):
	x1 = s1.split(".")
	x2 = s2.split(".")
	if all(x in x2 for x in x1): return True
	else: return False


def merge_section(arr):
	all_data = []
	current_arr = [arr[0]]
	i = 1
	while i < len(arr):
		if is_subsection(current_arr[0], arr[i]):
			current_arr.append(arr[i])
		else:
			all_data.append(current_arr)
			current_arr = [arr[i]]
		i += 1
	all_data.append(current_arr)
	return all_data


def text_cleaning(text):
	tokens = nltk.word_tokenize(text)
	return tokens


def tfidf_document_similarity(documents):
	tfidf_vectorizer = TfidfVectorizer(tokenizer = text_cleaning)
	tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
	doc_similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
	return doc_similarity


def compare_sections(section, concept):
	wiki_summary, wiki_content = get_wiki_data(concept)
	wiki_content = clean_text(wiki_content)
	documents = [wiki_content]
	for index in section:
		content = get_book_data(index)
		content = clean_text(content)
		documents.append(content)
	score = tfidf_document_similarity(documents)[0]
	max_score = score[1]
	index = 1
	for i in range(1, len(score)):
		if score[i] > max_score:
			max_score = score[i]
			index = i
	best_section = section[index-1]
	return best_section


def get_section_combination(arr):
	subsets = []
	for l in range(0, len(arr) + 1):
		for subset in itertools.combinations(arr, l):
			subsets.append(subset)
	subsets = [subsets[i] for i in range(1, len(subsets))]
	return subsets


def get_final_section_list(documents, section_combination, concept):
	wiki_summary, wiki_content = get_wiki_data(concept)
	wiki_content = clean_text(wiki_content)
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
	return best_section, max_score



def resolve_multi_sections(sections, concept):
	resulted_section = []
	documents = {}
	for section in sections:
		documents[section] = {
			"content": clean_text(get_book_data(section))
		}
	section_combination = get_section_combination(sections)
	# print(section_combination)
	resulted_section, max_score = get_final_section_list(documents, section_combination, concept)
	return resulted_section, max_score



def resolve_sections(sections, concept):
	section_list = merge_section(sections)
	resulted_section = []
	for section in section_list:
		if len(section) == 1:
			resulted_section.append(section[0])
		else:
			resulted_section.append(compare_sections(section, concept))
	return resulted_section


def sort_sections(file_name):
	title_match_data = read_concept_match(file_name)
	all_data = {}
	for i in range(len(title_match_data)):
	# for i in range(10):
		func_type = int(title_match_data[i]["type"])
		concept = title_match_data[i]["concept"]
		sections = title_match_data[i]["index"]
		if func_type == 1 or func_type == 2:
			print(i, title_match_data[i]["index"])
			hr_index = resolve_sections(sections, concept)
			mc_index, max_score = resolve_multi_sections(hr_index, concept)
			hr_index = "|".join(hr_index)
			mc_index = "|".join(mc_index)
		else:
			hr_index = ""
			mc_index = ""
			max_score = 0
		all_data[i] = {
			"concept": concept,
			"type": func_type,
			"index" : "|".join(sections),
			"hr_index": hr_index,
			"mc_index": mc_index,
			"score": max_score
		}
	return all_data


file_name = "../required_data/concept_title_match.csv"
output_file = "../required_data/resolve_concept_title_match.csv"
title_match_data = sort_sections(file_name)
save_concept_resolve_data(title_match_data, output_file)

