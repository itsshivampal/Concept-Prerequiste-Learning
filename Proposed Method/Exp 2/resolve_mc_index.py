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
	columns = ["concept", "type", "index", "hr_index", "mc_index", "score"]
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





def get_section_combination(arr):
	subsets = []
	for l in range(0, len(arr) + 1):
		for subset in itertools.combinations(arr, l):
			subsets.append(subset)
	subsets = [subsets[i] for i in range(1, len(subsets))]
	return subsets


def get_final_section_list(documents, section_combination, concept, wikipedia_data_file):
	wiki_summary, wiki_content = get_wiki_data(concept, wikipedia_data_file)
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



def resolve_multi_sections(sections, concept, wikipedia_data_file, book_content_file):
	resulted_section = []
	documents = {}
	for section in sections:
		documents[section] = {
			"content": clean_text(get_book_data(section, book_content_file))
		}
	section_combination = get_section_combination(sections)
	resulted_section, max_score = get_final_section_list(documents, section_combination, concept, wikipedia_data_file)
	return resulted_section, max_score








def sort_mc_sections(df, wikipedia_data_file, book_content_file):
	title_match_data = read_hr_index(df)
	all_data = {}
	for i in range(len(title_match_data)):
	# for i in range(10):
		func_type = int(title_match_data[i]["type"])
		concept = title_match_data[i]["concept"]
		sections = title_match_data[i]["index"]
		hr_index = title_match_data[i]["hr_index"]
		if func_type != 0:
			mc_index, max_score = resolve_multi_sections(hr_index, concept, wikipedia_data_file, book_content_file)
			mc_index = "|".join(mc_index)
		else:
			mc_index = ""
			max_score = 0
		all_data[i] = {
			"concept": concept,
			"type": func_type,
			"index" : "|".join(sections),
			"hr_index": "|".join(hr_index),
			"mc_index": mc_index,
			"score": max_score
		}
	df = save_concept_resolve_data(title_match_data)
	return df
