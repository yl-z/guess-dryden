'''
Open html of 12 books of the Aeneid from UMichigan (Dryden text) and split lines
Store as a dataframe in english.csv
functions are specific to the html format of the website
TODO: rebuild this and the latin cleaner to catch the 1-2 missing lines in each document due to formatting anomalies
hopefully make the algorithm more general so this is less of a hassle
'''

import re

import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser

executable_path = {'executable_path': '/Applications/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


def grab_data_umichigan(url, booknumber):
    '''pull text and split into lines; return dictionary of all lines in book, labeled by line number'''
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    b = soup.get_text()

    #generally break into lines and get rid of numbering, spaces
    b = b.replace(u'\xa0', u'*')
    lines = re.split("\n|\t|\*|[0-9]", b)
    lines = list(filter(None, lines))

    def f(x):  #remove illustration boxes and page # containers, being careful to keep normal text punctuation
        return (x != 'Page ') and (not (re.match(r"\W", x[0]))) or (re.match(r"[('\"]", x[0]))
    lines = list(filter(f, lines))

    #get rid of header and footer text, including the "argument" section as well, for now anyway (slight differences for each book)
    if (booknumber == 1):
        lines = lines[15:-2]
    else: lines = lines[14:-2]

    #label the lines
    my_dict = {}
    for i in range(0, len(lines)):
        my_dict[f"line{i+1}"] = lines[i]

    return my_dict


def umichiganDryden():
    '''pull twelve books; return dictionary with book number as key and lines list as values'''
    my_dict = {}
    urlleft = 'https://quod.lib.umich.edu/e/eebo/A65112.0001.001/1:20.'
    urlright = '?rgn=div2;view=fulltext'
    for i in range(1,13):
        bookurl = f"{urlleft}{i}{urlright}"
        lines = grab_data_umichigan(bookurl, i)
        my_dict[f"Book {i}"] = lines
    #print(my_dict)
    browser.quit()
    return my_dict


english = umichiganDryden()
df = pd.DataFrame(english)
df.to_csv('english.csv')
