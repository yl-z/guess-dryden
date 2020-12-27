"""
combine both texts with respective translations
output json files for later processing
            columns: booknum, linenum, linetext, translation
rows:
lines indexed by their number
"""
import six
import pandas as pd
from google.cloud import translate_v2 as translate

file1 = open("../scrapingdata/latin.csv", "r")
file2 = open("../scrapingdata/english.csv", "r")

sourceText = pd.read_csv(file1, index_col=0)
targetText = pd.read_csv(file2, index_col=0)

st = sourceText.T.stack()
st = st.to_frame(name="line")

tt = targetText.T.stack()
tt = tt.to_frame(name="line")


def translate_and_label(df, sl="la", tl="en"):
    """
    send translations as array for faster api interaction
    then label and retrieve data through a loop
    """
    cleanarr = []
    for i in range(len(df)):
        line = df.iloc[i].to_string(header=False,
                                    index=False, name=False).lstrip()
        cleanarr.append(line)

    translate_client = translate.Client()
    if isinstance(cleanarr, six.binary_type):
        cleanarr = cleanarr.decode("utf-8")
    result = translate_client.translate(cleanarr, source_language=sl,
                                        target_language=tl)

    ##

    outer_dict = {}
    for i in range(len(df)):
        line = df.iloc[i].to_string(header=False,
                                    index=False, name=False).lstrip()
        inner_dict = {}
        inner_dict["booknum"] = df.index[i][0]
        inner_dict["linenum"] = df.index[i][1]
        inner_dict["line"] = line
        inner_dict["translation"] = result[i]["translatedText"]
        outer_dict[i] = inner_dict

    df = pd.DataFrame(outer_dict)
    return df


datalat = translate_and_label(st.head(90))
datalat.to_json('../static/latin.js')

dataeng = translate_and_label(tt.head(128), sl="en", tl="la")
dataeng.to_json('../static/english.js')
