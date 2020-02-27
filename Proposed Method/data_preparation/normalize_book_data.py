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
    print(keyword1)
    keyword2 = clean_text(keyword2)
    print(keyword2)
    if keyword1 == keyword2:
        return True
    else:
        return False


def correct_content(content, keyword, concept):
    words = content.split(" ")
    words_len = len(words)
    keyword_len = len(keyword)
    i = 0
    new_content = []
    while i < words_len - keyword_len + 1:
        matching_word = " ".join(words[i:i+keyword_len])
        if match_text(matching_word, keyword):
            new_content.append(concept)
            i += keyword_len
        else:
            new_content.append(words[i])
            i += 1
    new_content = " ".join(new_content)
    return new_content




def main_function(book_data, keywords_data, output_file):
    df_book = pd.read_csv(book_data, encoding = "utf-8")
    df_keywords = pd.read_csv(keywords_data, encoding = "utf-8")
    pass


book_data = "output/physics_book_content.csv"
keywords_data = "output/physics_concepts_ambiguity.csv"
output_file = "output/final-book-content.csv"

# main_function(book_data, keywords_data, output_file)

content1 = "I am interested inke kinetic energy ink.e. in.k.e. kinetics energies kinetics energy energy kinetic"
content = "Kinetic Energy is ke and k.e. kinetics energies inke abc.k.e."
substitution = [['Kinetic Energy', 'k.e.'],
                ['Kinetic Energy', 'ke'],
                ['Kinetic Energy', 'kinetic energy']]

for pair in substitution:
    content = correct_content(content, pair[0], pair[1])
    print(content)



# text = "candy"
# print(porter_stemming(text))
# print(wordnet_lemmatization(text))

# keyword1 = "kinetic's energies"
# keyword2 = "kinetic energy"
# print(match_text(keyword1, keyword2))
