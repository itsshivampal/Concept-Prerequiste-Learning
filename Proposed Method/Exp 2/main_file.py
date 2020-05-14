import pandas as pd

from title_concept_matching import match_title_concept
from resolve_hr_index import sort_hr_sections


# Required Files
book_content_file = "../output_files/physics_normalized_content.csv"
labeled_pairs_file = "../output_files/physics_labeled_pairs.csv"
wikipedia_data_file = "../output_files/physics_correct_wikipedia_data.csv"
concepts_file = "../output_files/physics_concepts_ambiguity.csv"


# Step 1: Matching concepts with Title of book
df_match_data = match_title_concept(book_content_file, concepts_file)
df_match_data.to_csv("data/title_concept_match.csv")

# Step 2: Resolving Hierarchical ambiguity
df_match_data = pd.read_csv("data/title_concept_match.csv", encoding = "utf-8")
resolve_hr_data = sort_hr_sections(df_match_data)
resolve_hr_data.to_csv("data/resolve_hr_index.csv")

# Step 3: Resolve Multi Chapter Ambiguity