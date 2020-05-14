import pandas as pd

from title_concept_matching import match_title_concept

# Required Files
book_content_file = "../output_files/physics_normalized_content.csv"
labeled_pairs_file = "../output_files/physics_labeled_pairs.csv"
wikipedia_data_file = "../output_files/physics_correct_wikipedia_data.csv"
concepts_file = "../output_files/physics_concepts_ambiguity.csv"


df_match_data = match_title_concept(book_content_file, concepts_file)
print(df_match_data)
