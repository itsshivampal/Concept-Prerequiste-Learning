**Add all your codes in Codes Folder**

# Steps for Data Processing

## Step 1: Conversion of PDF to TXT
**Text Files**: These files are created from "Required Data" folder's pdf files using the library "*PDFMiner*".<br/>
Use command - **pdf2txt -A -o file_name.txt file_name.pdf** to convert chapters, ToCs and index files

## Step 2: Data Cleaning and formating
Manually clean the above extracted text files for removing junk data like extra new lines, special characters, ligatures, unaligned format, etc. and bring files to the required format
For removing ligatures, use ligatures.txt files and replace their character with suitable characters.
Do all the editing in the same files.

## Step 3: Index Data Extraction
In this step we need to extract the data and generate a CSV file corresponding to each book's text file and save in "Index Data" folder
Run the code -> **Codes/index_data_extraction.ipynb**

## Step 4: Finding Acronym and Abbreviation
Find the abbreviations and acronyms used for each topic in index data from book chapters data


## Step 5: Merging all the topics of index files
Using the data got in above steps, merge all the topics and create a final csv file contaning each and unique terms

## Step 6: Division of book chapters data corresponding to each Table of Content entry



# Task Done
Step 1 <br/>
Step 2 <br/>
Step 3 <br/>

# Ongoing Tasks
Step 6 <br/>


# Pending Task
Step 4 <br/>
Step 5 <br/>