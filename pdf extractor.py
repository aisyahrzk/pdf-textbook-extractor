import pdfplumber
import io
import re
import pandas as pd
import numpy as np
import string

chapter = ''
topic = ''
page_num = ''
past_line = ''
content = ''
filepath_stopwords = "stopwords-ms.txt"


def get_stopwords(path):

    with open(path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return list(frozenset(stop_set))

stopwords = get_stopwords(filepath_stopwords)

def preprocess_content(text):
    text = str(text)
    text = " ".join(text.splitlines())
    text = re.sub(' +', ' ', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    # Remove stop words and punctuation
    tokens = text.split(" ")
    token_filter = [token.lower() for token in tokens if token not in string.punctuation]
    text = (" ").join(token_filter)

    return text

book = pd.DataFrame(columns = ["chapter", "topic", "page_num","content"])

# change this index based on the textbook specific isi kandungan page
index_page = [4,5]

for x in index_page:
    with pdfplumber.open(r'textbook\sej-ting-5.pdf') as pdf:
        first_page = pdf.pages[x]
        result = first_page.extract_text()
    filename = "isi_kandungan.txt"
    with io.open(filename, 'a+', encoding='utf8') as f:
        f.write(result)


#parse data to form a dataset to extract data from specific pages
# Using readlines()
index_buku = open('isi_kandungan.txt', 'r')
Lines = index_buku.readlines()
  
count = 0
past = False

# preprocess isi kandungan extracted document, get chapter name, topic and page number
for line in Lines:
    line = line.strip()
    line = line.replace("iivv","")


    if re.search(r'\bBab\b', line) != None: # for chapter lines
        chapter = re.sub(r'[^a-zA-Z ]+', '',line)
        topic = ''
        page_num = ''
    elif (line[-1:].isdigit()): # for lines with page number
        page_num = next(re.finditer(r'\d+$', line)).group(0)
        #topic_num = re.findall('^[0-9]*\.[0-9]+.*$',line)
        topic = re.sub(r'\d+', '', line)
    else:
        topic = ''
        page_num = ''

    page = {'chapter': chapter, 'topic': topic, 'page_num': page_num}
    book = book.append(page, ignore_index = True)


# clean extracted data
book['topic'] = book['topic'].apply(lambda x: re.sub(r'[^A-Za-z ]+', '', x))

book = book.replace(r'^\s*$', np.nan, regex=True)

book = book[pd.notnull(book['page_num'])]

book = book.reset_index(drop = True)


df = pd.DataFrame(columns = ["chapter", "topic", "page_num","content"])


#extract content from page num for each topic
for x in range(len(book)-1):

    content = ''


    for j in range(int(book.loc[x,'page_num'])+9,int(book.loc[x+1,'page_num'])+9):
        with pdfplumber.open(r'textbook\sej-ting-5.pdf') as pdf:
            page = pdf.pages[j]
            result = page.extract_text()
            content= content + result
            

        for line in result.splitlines():
            chapter = book.loc[x,'chapter']
            topic = book.loc[x,'topic']
            page_num = j - 9
            page = {'chapter': chapter, 'topic': topic,'page_num': page_num,'content':line}
            df = df.append(page, ignore_index = True)
    book.loc[x,'content'] = content

df = df.loc[df["content"].str.count(" ") >= 2]      
df['content'] = df['content'].apply(lambda x: preprocess_content(x))
book = book.loc[book["content"].str.count(" ") >= 2]
book['content'] = book['content'].apply(lambda x: preprocess_content(x))


df.to_excel('sejarah_f5.xlsx')
book.to_excel('isi_f5.xlsx')

