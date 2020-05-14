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
	columns = ["concept", "type", "index", "hr_index"]
	df = pd.DataFrame(columns = columns)
	for i in range(len(data)):
		df = df.append(data[i], ignore_index = True)
	return df


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


def compare_sections(section, concept, wikipedia_data_file, book_content_file):
	wiki_summary, wiki_content = get_wiki_data(concept, wikipedia_data_file)
	wiki_content = clean_text(wiki_content)
	documents = [wiki_content]
	for index in section:
		content = get_book_data(index, book_content_file)
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





def resolve_sections(sections, concept, wikipedia_data_file, book_content_file):
	section_list = merge_section(sections)
	resulted_section = []
	for section in section_list:
		if len(section) == 1:
			resulted_section.append(section[0])
		else:
			resulted_section.append(compare_sections(section, concept, wikipedia_data_file, book_content_file))
	return resulted_section


def sort_hr_sections(df_file, wikipedia_data_file, book_content_file):
	title_match_data = read_concept_match(df_file)
	all_data = {}
	for i in range(len(title_match_data)):
	# for i in range(10):
		func_type = int(title_match_data[i]["type"])
		concept = title_match_data[i]["concept"]
		sections = title_match_data[i]["index"]
		if func_type != 0:
			hr_index = resolve_sections(sections, concept, wikipedia_data_file, book_content_file)
			hr_index = "|".join(hr_index)
		else:
			hr_index = ""
		all_data[i] = {
			"concept": concept,
			"type": func_type,
			"index" : "|".join(sections),
			"hr_index": hr_index,
		}
	df = save_concept_resolve_data(all_data)
	return df
