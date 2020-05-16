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






def get_best_section(concept, title_section, content_section, wikipedia_data_file, book_content_file):
    wiki_summary, wiki_content = get_wiki_data(concept, wikipedia_data_file)
    wiki_content = clean_text(wiki_content)
    all_documents = [wiki_content]

    content = get_book_data(title_section, book_content_file)
    content = clean_text(content)
    all_documents.append(content)

    content = get_book_data(content_section, book_content_file)
    content = clean_text(content)
    all_documents.append(content)

    score = tfidf_document_similarity(all_documents)[0]
    if score[1] > score[2]: return 1
    else: return 2



def get_section_order(concept, title_section, content_section, wikipedia_data_file, book_content_file):
    final_section = ""
    final_order = ""
    if title_section.isna().values[0]: title_section = ""
    else: title_section = title_section.values[0]

    if content_section.isna().values[0]: content_section = ""
    else: content_section = content_section.values[0]

    if title_section == "":
        final_order = content_section
    else:
        if content_section == "":
            final_section = title_section
            final_order = title_section
        else:
            section = get_best_section(concept, title_section, content_section, wikipedia_data_file, book_content_file)
            if section == 1:
                final_section = title_section
                final_order = content_section
            elif section == 2:
                final_section = content_section
                final_order = content_section
    return final_section, final_order



def sort_book_section_ambiguity(df, wikipedia_data_file, book_content_file):
	for i in range(df.shape[0]):
	# for i in range(30):
		concept = df[["concept"]].iloc[i].values[0]

		title_section = df[["book1_title"]].iloc[i]
		content_section = df[["book1_content"]].iloc[i]
		book1_final_section, book1_final_order = get_section_order(concept, title_section, content_section, wikipedia_data_file, book_content_file)
		df.at[i, "book1_fs"] = book1_final_section
		df.at[i, "book1_fo"] = book1_final_order

		title_section = df[["book2_title"]].iloc[i]
		content_section = df[["book2_content"]].iloc[i]
		book2_final_section, book2_final_order = get_section_order(concept, title_section, content_section, wikipedia_data_file, book_content_file)
		df.at[i, "book2_fs"] = book2_final_section
		df.at[i, "book2_fo"] = book2_final_order

		title_section = df[["book3_title"]].iloc[i]
		content_section = df[["book3_content"]].iloc[i]
		book3_final_section, book3_final_order = get_section_order(concept, title_section, content_section, wikipedia_data_file, book_content_file)
		df.at[i, "book3_fs"] = book3_final_section
		df.at[i, "book3_fo"] = book3_final_order
	return df
