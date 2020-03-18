# Book Data Collection

This folder has 3 scripts

## Initial Step

Clean the "physics-grade.toc"


## Script 1: get_book_toc.py

toc_file = "../../dataset/physics-grade.toc"
output_file = "physics_toc.csv"
output_txt_file = "physics_toc.txt"

This script will produce "physics_toc.txt" and its csv file as well in the same folder

## Next Step: Manually scrap data from book

Copy "physics_toc.txt" -> "physics_book.txt" and save all the scrapped data in this file

## Script 2: book_content_cleaning.py

input_file = "physics_book.txt"
output_csv_file = "physics_book_content.csv"

This script read the input_file and save the data in CSV file


## Script 3: normalise_book_data.py

book_data = "physics_book_content.csv"
keywords_data = "../../output_files/physics_concepts_ambiguity.csv"
output_file_csv = "../../output_files/physics_normalized_content.csv"
output_file_txt = "physics_normalized_content.txt"

This script read book_data and keywords_data and produce output_files which contain following columns
- section
- title
- page_no
- content
- normalise_content
- highlight_content

Save the final output in output_files directory
