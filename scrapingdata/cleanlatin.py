'''
Open html of 12 books of the Aeneid from latin library (Latin text), split lines,
Store as a dataframe in latin.csv
functions are specific to the html
'''

import pandas as pd
import re
from splinter import Browser
from bs4 import BeautifulSoup

executable_path = {'executable_path': '/Applications/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


def grab_data_latinLibrary(url):
    '''pull text and split into lines; return dictionary of all lines in book, labeled by line number'''
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    a = soup.get_text()

    #generally break into lines and get rid of numbering and spaces
    a = a.replace(u'\xa0', u'*')
    lines = re.split("\n|\t|\*|[0-9]", a)
    lines = list(filter(None, lines))
    def f(x):
        return (x != ' ')
    lines = list(filter(f, lines))

    #get rid of header and footer text
    lines = lines[2:-3]

    #label the lines
    my_dict = {}
    for i in range(0, len(lines)):
        my_dict[f"line{i+1}"] = lines[i]

    return my_dict


def latinLibraryVergil():
    '''pull twelve books; return dictionary with book number as key and lines list as values'''
    my_dict = {}
    url = 'https://www.thelatinlibrary.com/verg'
    for i in range(1,13):
        bookurl = f"{url}il/aen{i}.shtml"
        lines = grab_data_latinLibrary(bookurl)
        my_dict[f"Book {i}"] = lines
    #print(my_dict)
    browser.quit()
    return my_dict


latin = latinLibraryVergil()
df = pd.DataFrame(latin)
df.to_csv('latin.csv')


"""
#checks
for book in latin:
    #print(latin[book][0:5])
    #print(latin[book][-5:])
    print(len(latin[book]))
#should be: 756, 804, 718, 705, 871, 901, 817, 731, 818, 908, 915, 952
"""
