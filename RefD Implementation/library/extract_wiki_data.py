'''
Extracting Wikipedia Content

For using this library, import extract_wikipedia_data
and use function - extract_wikipedia_data(topic)
for extracting wikipedia data for that topic
'''

import wikipedia

def contain_section(line):
    line = line.strip()
    if len(line) > 4:
        if line[0] == "=" and line[1] == "=" and line[-2] == "=" and line[-1] == "=":
            return True
        else:
            return False


def wiki_section_extract(content):
    lines = content.split("\n")
    sections = ""
    for line in lines:
        if contain_section(line):
            sections += line[3:-3] + "\n"
    return sections.strip()


def keyword_data(topic = "", wiki_title = "", wiki_summary = "",
                 wiki_content = "", wiki_html = "", wiki_links = "", wiki_sections = ""):
    data = {
        'topic': topic,
        "wiki_title": wiki_title,
        "wiki_summary": wiki_summary,
        "wiki_content": wiki_content,
        "wiki_html": wiki_html,
        "wiki_links": wiki_links,
        "wiki_sections": wiki_sections
    }
    return data


def wiki_data_list():
    wiki_list = ['topic', 'wiki_title', 'wiki_summary', 'wiki_content', 'wiki_html', 'wiki_links', 'wiki_sections']
    return wiki_list


def extract_wikipedia_data(topic):
    wiki_title = ""
    wiki_summary = ""
    wiki_content = ""
    wiki_html = ""
    wiki_links = ""
    wiki_sections = ""
    try:
        wiki = wikipedia.search(topic)[0]
        try:
            wiki_data = wikipedia.page(wiki)
            wiki_title = wiki_data.title
            wiki_summary = wiki_data.summary
            wiki_content = wiki_data.content
            wiki_html = wiki_data.html()
            wiki_links = wiki_data.links
            wiki_sections = wiki_section_extract(wiki_content)

        except wikipedia.exceptions.DisambiguationError as e:
            print("blank")
        except wikipedia.exceptions.PageError as e:
            print("blank")

    except IndexError:
        print("blank")


    data = keyword_data(topic, wiki_title, wiki_summary,
                        wiki_content, wiki_html, wiki_links, wiki_sections)

    return data


def get_list_wiki_data(all_keywords):
    list_len = len(all_keywords)
    all_keyword_data = {}
    for i in range(list_len):
        all_keyword_data[i] = extract_wikipedia_data(all_keywords[i])
        print(i)
    return all_keyword_data
