import pandas as pd
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from load_data import *
from text_cleaning import clean_text
import re



def save_match_data(matching_data, output_file):
    df_match_data = pd.DataFrame(columns = ["concept", "index", "type"])
    for i in range(len(matching_data)):
        df_match_data = df_match_data.append(matching_data[i], ignore_index = True)
    df_match_data.to_csv(output_file)
    return True


def direct_matching(title, concept):
    title = clean_text(title).split(" ")
    concept = clean_text(concept).split(" ")
    if set(concept).issubset(set(title)) and len(concept) == len(title):
        return True
    else:
        return False

def concept_in_title(title, concept):
    title = clean_text(title).split(" ")
    concept = clean_text(concept).split(" ")
    if set(concept).issubset(set(title)):
        return True
    else:
        return False


def title_in_concept(title, concept):
    title = clean_text(title).split(" ")
    concept = clean_text(concept).split(" ")
    if set(title).issubset(set(concept)):
        return True
    else:
        return False


def matching_function(title, concept, key_terms, func_type):
    if func_type == 1:
        if direct_matching(title, concept):
            return True
        else:
            flag = 0
            for key_term in key_terms:
                if direct_matching(title, key_term):
                    flag = 1
                    break
            if flag: return True
            else: return False

    elif func_type == 2:
        if concept_in_title(title, concept):
            return True
        else:
            flag = 0
            for key_term in key_terms:
                if concept_in_title(title, key_term):
                    flag = 1
                    break
            if flag: return True
            else: return False

    elif func_type == 3:
        if title_in_concept(title, concept):
            return True
        else:
            flag = 0
            for key_term in key_terms:
                if title_in_concept(title, key_term):
                    flag = 1
                    break
            if flag: return True
            else: return False

#--------------------------------------------------------------------#

def match_title_concept():
    book_data = read_book_data()
    concept_data = read_concepts_file()
    matching_data = {}
    index = 0

    for i in range(len(concept_data)):
        concept = concept_data[i]["concept"]
        key_terms = concept_data[i]["key_terms"].split("|")
        matched_index = []

        for j in range(len(book_data)):
            title = book_data[j]["title"]
            if matching_function(title, concept, key_terms, func_type = 1):
                section = book_data[j]["section"]
                matched_index.append(section)

        if len(matched_index) == 0:
            for j in range(len(book_data)):
                title = book_data[j]["title"]
                if matching_function(title, concept, key_terms, func_type = 2):
                    section = book_data[j]["section"]
                    matched_index.append(section)
            if len(matched_index) == 0:
                for j in range(len(book_data)):
                    title = book_data[j]["title"]
                    if matching_function(title, concept, key_terms, func_type = 3):
                        section = book_data[j]["section"]
                        matched_index.append(section)
                if len(matched_index) == 0:
                    concept_type = 0
                else:
                    concept_type = 3
            else:
                concept_type = 2
        else:
            concept_type = 1

        print(i)

        matching_data[index] = {
            "concept": concept,
            "index": "|".join(matched_index),
            "type": concept_type
        }
        index += 1
    return matching_data

matching_data = match_title_concept()
output_file = "data/concept_title_match.csv"
save_match_data(matching_data, output_file)

