## Code 1: get_key_concepts.py

pairs_file = "../../dataset/physics.pairs"
wiki_terms = "../../dataset/physics-grade.wikis_clean"
output_location = "physics_concepts.csv"

This code read pairs file and wiki_terms, and output physics_concepts.csv in the same directory

-------------------------------------------------------

## Next Step: Copy "physics_concepts.csv" as "physics_key_concepts.csv"
Edit this file manually and remove useless terms

-------------------------------------------------------

Code 2: concept_disambiguation.py

key_concepts_file = "physics_key_concepts.csv"
output_location = "../../output_files/physics_concepts_ambiguity.csv"

This code read key_concepts_file and save final output in output_files directory as output_location
