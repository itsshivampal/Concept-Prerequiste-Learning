import pandas as pd

from title_concept_matching import match_title_concept
from resolve_hr_index import sort_hr_sections
from resolve_mc_index import sort_mc_sections
from concept_match_index import get_index_from_content
from sort_book_section import sort_book_section_ambiguity
from content_processing import get_concept_content
from concept_tfidf_score import get_tfidf_score
from concept_ranking import get_concept_ranking
from rank_filter import apply_rank_filter
from find_hidden_pairs import get_all_prereq_pairs
from calculate_prereq_val import get_labeled_prereq_val
from result_evaluation import graph_plotting


# Required Files
book_content_file = "../output_files/physics_normalized_content.csv"
labeled_pairs_file = "../output_files/physics_labeled_pairs.csv"
wikipedia_data_file = "../output_files/physics_correct_wikipedia_data.csv"
concepts_file = "../output_files/physics_concepts_ambiguity.csv"
wiki_tfidf_matrix = "../output_files/wiki_tfidf_matrix.csv"
testing_data = "../output_files/testing_data.csv"

chapter_distribution = [[2, 3, 4, 5, 6, 7, 8, 9, 10],
                        [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                        [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]]

# Step 1: Matching concepts with Title of book
# df_match_data = match_title_concept(book_content_file, concepts_file)
# df_match_data.to_csv("data/title_concept_match.csv")

# Step 2: Resolving Hierarchical ambiguity
# df_match_data = pd.read_csv("data/title_concept_match.csv", encoding = "utf-8")
# resolve_hr_data = sort_hr_sections(df_match_data, wikipedia_data_file, book_content_file)
# resolve_hr_data.to_csv("data/resolve_hr_index.csv")

# Step 3: Resolve Multi Chapter Ambiguity
# resolve_hr_data = pd.read_csv("data/resolve_hr_index.csv", encoding = "utf-8")
# resolve_mc_data = sort_mc_sections(resolve_hr_data, chapter_distribution, wikipedia_data_file, book_content_file)
# resolve_mc_data.to_csv("data/resolve_mc_index.csv")


# Step 4: Get index of  content through content
# resolve_mc_data = pd.read_csv("data/resolve_mc_index.csv", encoding = "utf-8")
# final_indexing_file = get_index_from_content(book_content_file, resolve_mc_data, chapter_distribution)
# final_indexing_file.to_csv("data/final_index_file.csv")


# Step 5: Get final sections of each concept from each book
# final_indexing_file = pd.read_csv("data/final_index_file.csv")
# sorted_concept_sections = sort_book_section_ambiguity(final_indexing_file, wikipedia_data_file, book_content_file)
# sorted_concept_sections.to_csv("data/sorted_final_concepts.csv")


# Step 6: Extracting Content for Concepts
# sorted_concept_sections = pd.read_csv("data/sorted_final_concepts.csv")
# concept_content = get_concept_content(sorted_concept_sections, book_content_file)
# concept_content.to_csv("data/concept_content.csv")


# Step 7: Finding the universal ranking of concepts in book
# sorted_concept_sections = pd.read_csv("data/sorted_final_concepts.csv")
# concept_ranking = get_concept_ranking(sorted_concept_sections, book_content_file)
# concept_ranking.to_csv("data/concept_rank.csv")


# Step 8: Apply Rank filtering on extracted concepts
# concept_ranking = pd.read_csv("data/concept_rank.csv")
# concept_content = pd.read_csv("data/concept_content.csv")
# rank_filtered_concepts = apply_rank_filter(concept_content, concept_ranking)
# rank_filtered_concepts.to_csv("data/rank_filtered_concepts.csv")


# Step 9: Finding TF-IDF score of each concept in each document
# rank_filtered_concepts = pd.read_csv("data/rank_filtered_concepts.csv")
# tfidf_score = get_tfidf_score(rank_filtered_concepts)
# tfidf_score.to_csv("data/content_tfidf_score.csv")


# Step 10: Get in-depth prereq pairs
# tfidf_score = pd.read_csv("data/content_tfidf_score.csv")
# all_prereq_pairs = get_all_prereq_pairs(tfidf_score)
# all_prereq_pairs.to_csv("data/all_prereq_pairs.csv")


# Step 11: Result Prediction for labeled pairs
# df_prereq_pairs = pd.read_csv("data/all_prereq_pairs.csv")
# df_wiki_tfidf = pd.read_csv(wiki_tfidf_matrix)
# df_labeled_pairs = pd.read_csv(labeled_pairs_file)
# labeled_prereq_val = get_labeled_prereq_val(df_labeled_pairs, df_prereq_pairs, df_wiki_tfidf)
# labeled_prereq_val.to_csv("data/predicted_prereq.csv")

# Step 12: Graph plotting of predicted results
# df_labeled_prereq = pd.read_csv("data/predicted_prereq.csv")
# graph_plotting(df_labeled_prereq, file_name = "data/curve_all.png")


#---------------------------------
# Comparing results with testing data
df_prereq_pairs = pd.read_csv("data/all_prereq_pairs.csv")
df_wiki_tfidf = pd.read_csv(wiki_tfidf_matrix)
df_testing_data = pd.read_csv(testing_data)
df_testing = df_testing_data[["topic_a", "topic_b", "relation"]]
df_labeled_prereq = get_labeled_prereq_val(df_testing, df_prereq_pairs, df_wiki_tfidf)

df_labeled_prereq.to_csv("data/test_data_pred.csv")
graph_plotting(df_labeled_prereq, file_name = "data/curve_test.png")
