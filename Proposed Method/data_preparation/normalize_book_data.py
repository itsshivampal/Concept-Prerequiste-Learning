import pandas as pd
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import re

def porter_stemming(text):
    porter_stemmer  = PorterStemmer()
    word_tokens = text.split(" ")
    words = [porter_stemmer.stem(word) for word in word_tokens]
    new_text = " ".join(words)
    return new_text


def wordnet_lemmatization(text):
    wordnet_lemmatizer = WordNetLemmatizer()
    word_tokens = text.split(" ")
    words = [wordnet_lemmatizer.lemmatize(word) for word in word_tokens]
    new_text = " ".join(words)
    return new_text


def remove_punctuations(text):
    new_text = ""
    punctuations = "!\"#$%&()*+-.,:;<=>?@[\]^_'{|}~"
    for ch in text:
        if ch not in punctuations:
            new_text += ch
    return new_text


def clean_text(content):
    content = content.lower()
    content = re.sub(r'\d+', '', content)
    content = remove_punctuations(content)
    content = porter_stemming(content)
    # content = wordnet_lemmatization(content)
    content = content.strip()
    return content

def match_text(keyword1, keyword2):
    keyword1 = clean_text(keyword1)
    keyword2 = clean_text(keyword2)
    if keyword1 == keyword2:
        return True
    else:
        return False


def correct_content(content, keyword, concept):
    if content == "":
        return content
    words = content.split(" ")
    words_len = len(words)
    keyword_len = len(keyword.split())
    if words_len < keyword_len:
        return content
    else:
        i = 0
        new_content = []
        while i < words_len - keyword_len + 1:
            matching_word = " ".join(words[i:i+keyword_len])
            if match_text(matching_word, keyword):
                print(keyword, concept)
                new_content.append(concept)
                i += keyword_len
            else:
                new_content.append(words[i])
                i += 1
        if i < words_len:
            while i < words_len:
                new_content.append(words[i])
                i += 1
        new_content = " ".join(new_content)
        return new_content

def read_keyword_file(file_name):
    df_keywords = pd.read_csv(file_name, encoding = "utf-8")
    all_data = {}
    for i in range(df_keywords.shape[0]):
        wiki_terms = df_keywords[["key_terms"]].iloc[i].values[0]
        wiki_terms = wiki_terms.split("|")
        keywords = [clean_text(term) for term in wiki_terms]
        keywords = "|".join(keywords)
        concept = df_keywords[["concept"]].iloc[i].values[0]
        all_data[i] = {
            "concept": concept,
            "keywords": keywords
        }
    # print(df_keywords[["key_terms"]].iloc[1].values[0])
    # print(all_data[1]["keywords"])
    return all_data

def remove_ambiguity(content, data):
    for i in range(len(data)):
        keywords = data[i]["keywords"]
        keywords = keywords.split("|")
        for keyword in keywords:
            content = correct_content(content, keyword, data[i]["concept"])
    return content


def save_text_file(df, output_file):
    file = open(output_file, "w+")
    for i in range(df.shape[0]):
        section = str(df[["section"]].iloc[i].values[0])
        title = str(df[["title"]].iloc[i].values[0])
        page_no = str(df[["page_no"]].iloc[i].values[0])
        content = str(df[["content"]].iloc[i].values[0])
        line = section + "|" + title + "|" + page_no + "\n"
        file.write(line)
        file.write(content)
        file.write("\n---------------------------------------------------------\n\n")
    file.close()
    return True



def main_function(book_data, keywords_data, output_file_csv, output_file_txt):
    concept_data = read_keyword_file(keywords_data)
    df_book = pd.read_csv(book_data, encoding = "utf-8")

    for i in range(df_book.shape[0]):
        content = df_book[["content"]].iloc[i]
        if content.isna().values[0] == True:
            new_content = ""
        else:
            content = content.values[0]
            new_content = remove_ambiguity(content, concept_data)
        df_book.at[i, "content"] = new_content

    df_book.to_csv(output_file_csv)
    save_text_file(df_book, output_file_txt)
    return True


book_data = "output/physics_book_content.csv"
keywords_data = "output/physics_concepts_ambiguity.csv"
output_file_csv = "output/physics-normalized-content.csv"
output_file_txt = "output/physics-normalized-content.txt"

main_function(book_data, keywords_data, output_file_csv, output_file_txt)
