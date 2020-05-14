import nltk
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
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


def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    sentence = " ".join(filtered_sentence)
    return sentence


def remove_punctuations(text):
    new_text = ""
    punctuations = "!\"#$%&()*+-.,:;<=>?@[\]^_{|}~"
    for ch in text:
        if ch not in punctuations:
            new_text += ch
        else:
            new_text += " "
    return new_text


def clean_text(content):
    content = content.lower()
    content = re.sub(r'\d+', '', content)
    content = remove_punctuations(content)
    content = remove_stopwords(content)
    content = content.replace(" \'", "\'")
    # content = porter_stemming(content)
    content = wordnet_lemmatization(content)
    content = content.strip()
    return content


