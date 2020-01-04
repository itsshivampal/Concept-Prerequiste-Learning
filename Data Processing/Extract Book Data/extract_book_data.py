'''
This code is built in python 3.

Following code will extract book data as per ToC section of book
and save all the data in CSV as well as JSON format
having 3 columns:
- Section: Section or sub chapter or sub topic number in ToC
- Title: Title of the section
- Content: Content which mention in book under that section

'''

# libraries need to install

import re
import os
import json
import pandas as pd


# required files for data extraction
toc_file = "required_data/prml_toc.txt"
chapter_data = "required_data/prml_booktext.txt"


# Reading ToC file
def read_toc():
	toc_array = []
	file = open(toc_file)
	for line in file:
		line = line.strip()
		if line != "\n" and re.search('[a-zA-Z0-9]', line):
			toc_array.append(line)
	file.close()
	return toc_array


# Reading book's chapter data
def read_book():
	book_array = []
	file = open(chapter_data)
	for line in file:
		line = line.strip()
		if line != "\n" and re.search('[a-zA-Z0-9]', line):
			book_array.append(line)
	file.close()
	return book_array


############## Functions for separting text into files ##############

# Function for striping toc section line
def data_separation(line):
	line = line.strip()
	pos = line.find(" ")
	index_num = line[:pos]
	title = line[pos+1:]
	return (index_num, title)


# Function for creating files in required directory
def create_file(line):
	line = line.replace(" ", "_")
	file_name = "book_data/" + line + ".txt"
	file = open(file_name, "w+")
	file.close()
	return file_name


# Function for matching toc line in book line for section break
def match_line(line1, line2):
	line1 = line1.lower()
	line2 = line2.lower()
	index1, title = data_separation(line1)
	if index1 in line2 or index1+"." in line2:
		if title in line2: return 1
		else: return 0
	else:
		return 0


# main function for separting all the data
def create_separate_files(toc_array, book_array):
	toc_len = len(toc_array)
	book_len = len(book_array)

	i = 0

	current_line = toc_array[i]
	next_line = toc_array[i + 1]

	file_name= create_file(current_line)
	current_file = open(file_name, "a")

	for j in range(book_len):
		line = book_array[j]
		if match_line(next_line, line):
			if i < toc_len - 2:
				i += 1
				current_line = toc_array[i]
				next_line = toc_array[i + 1]
			else:
				current_line = toc_array[toc_len - 1]
			current_file.close()
			file_name = create_file(current_line)
			current_file = open(file_name, "a")
		else:
			line += "\n"
			current_file.write(line)
        
	current_file.close()

	return True

def data_in_dictionary(toc_array):
	book_data = {}
	i = 0

	for topic in toc_array:
		index_num, title = data_separation(topic)
		topic = topic.replace(" ", "_")
		file_name = "book_data/" + topic + ".txt"
		file = open(file_name, "r")
		content = file.read()
		file.close()
		data = {
			'Section': index_num,
			'Title': title,
			'Content': content
		}
		book_data[i] = data
		i += 1
	return book_data


############## End ##############



############## Following functions for cleaning the data ##############

def add_line(content, line, state):
	line = line.strip()
	if state == True:
		content += " " + line
	else: content += line
	return content


def incomplete_words(content):
	content_array = content.split("\n")
	state = True
	new_content = ""
	for i in range(len(content_array)-1):
		if content_array[i][-1] == "-":
			new_content = add_line(new_content, content_array[i][:-1], state)
			state = False
		else:
			new_content = add_line(new_content, content_array[i], state)
			state = True
	new_content = new_content.strip()
	return new_content


def handle_special_char(content):
	new_content = ""
	punctuations = "!\"#$%&()*+-.,:;<=>?@[]^_`{|}~"
	for ch in content:
		if ch == "'": ch = ""
		if ch in punctuations: ch = " "
		if ord(ch) < 97 or ord(ch) > 122: ch = " "
		new_content += ch
	return new_content


def handle_words(content):
	words = content.split(" ")
	new_list = [word for word in words if len(word) > 2]
	content = " ".join(new_list)
	return content


def clean_content(content):
	content = content.lower()
	content = incomplete_words(content)
	content = handle_special_char(content)
	content = re.sub("  +" , " ", content)
	content = handle_words(content)
	return content


def clean_dict_data(book_data):
	for i in range(len(book_data)):
		book_data[i]["Content"] = clean_content(book_data[i]["Content"])
	return book_data

############## End ##############


############## Following functions for saving the data ##############

def save_json(book_data):
	with open('output_data/book_data.json', 'w') as file:
		json.dump(book_data, file)


def save_csv(book_data):
	df = pd.DataFrame(columns=['Section', 'Title', 'Content'])
	for i in range(len(book_data)):
		df = df.append(book_data[i], ignore_index=True)
	df.to_csv("output_data/book_data.csv")

############## End ##############

#--------------------------------------------------------------------------#
#--------------------------------------------------------------------------#



# main function
def main_function():
	toc_array = read_toc()
	book_array = read_book()
	create_separate_files(toc_array, book_array)
	book_data = data_in_dictionary(toc_array)
	book_data = clean_dict_data(book_data)
	save_json(book_data)
	save_csv(book_data)

main_function()