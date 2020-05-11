import pandas as pd

wikipedia_data = "../output_files/physics_correct_wikipedia_data.csv"
book_data = "../output_files/physics_normaalised_content.csv"

df_wiki = pd.read_csv(wikipedia_data, encoding = "utf-8")
df_book = pd.read_csv(book_data, encoding = "utf-8")

