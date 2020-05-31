# Proposed Method

Files should be run in the following order:

## Step 1: Data Preparation - data_preparation/
/get_labeled_pairs
/get_wiki_data
/get_concepts
/get_book_data

## Step 2: Concept Content -
concept_content/title_concept_matching.py
concept_content/resolve_hr_index.py
concept_content/resolve_mc_index.py
concept_content/resolve_single_index.py

## Step 3: Concept Ranking
concept_ranking/concept_match_index.py
concept_ranking/concept_index_rank.py

## Step 4: Concept Prerequisites
concept_prereqs/content_processing.py
concept_prereqs/filtering_rank_theta.py
concept_prereqs/tf_idf_matrix.py
concept_prereqs/resolve_hidden_pairs.py


## Step 5: Baseling Results
refd_method/wiki_tfidf_values.py
refd_method/refd_calculation.py


## Step 6: Prerequisite Evaluation
prereq_evaluation/content_processing.py


## Step 7: Evaluate your results

