import spacy
from spacy.tokens import Doc
from spacy.vocab import Vocab

nlp = spacy.load("en_core_web_sm")

book_text = open("book_chapters_txt/bprml.txt").read()
doc = nlp(book_text)

print(len(doc))