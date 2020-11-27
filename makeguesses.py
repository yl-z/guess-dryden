"""
Matches translations, considering each book wholistically
For now this uses a simple string similarity measure
writes to (and calls) the same files as loadtranslations.py, and should be run after it
"""
import numpy as np
import pandas as pd
import textdistance

RESOLUTION = 0.1  # Controls how far the search looks for a similar line

file1 = open("static/english.js")
file2 = open("static/latin.js")

sourceText = pd.read_json(file1)
targetText = pd.read_json(file2)

sourceTextDict = sourceText.to_dict()
targetTextDict = targetText.to_dict()


def similarity(text1, text2):
    """
    return a number
    """
    return textdistance.jaro_winkler(text1, text2)


def find_relevant_range(sourcelinenum, sourcedoc, targetdoc):
    """
    scale the two documents to the same number of lines, and
    give the place corresponding to source line in target, with a range
    """
    center = round(sourcelinenum/len(sourcedoc)*len(targetdoc))
    span = round(len(targetdoc)*RESOLUTION)
    return max(center - span, 0), min(center + span, len(targetdoc))


def distribution(d1, d2):
    """
    Append new col containing lists of weights representing similarity to each line in relevant range
    Do this for d1[line] -> d2[translation] and d1[translation] -> d2[lines] (both one-to-many)
    Note that this function is not symmetric
    Working on dictionaries
    """
    for i in range(len(d1)):
        minindex, maxindex = find_relevant_range(i, d1, d2)
        d1[i]["linksToLines"] = np.array([])
        d1[i]["linksToTrans"] = np.array([])
        for j in range(minindex, maxindex):
            # match d1 translations with d2 original
            d1[i]["linksToLines"] = np.append(d1[i]["linksToLines"], similarity(d1[i]["translation"], d2[j]["line"]))
            # match d1 line with d2 translations
            d1[i]["linksToTrans"] = np.append(d1[i]["linksToTrans"], similarity(d1[i]["line"], d2[j]["translation"]))
    return d1


def summarystats(d):
    """
    compute average and difference of the linkages
    Working on dictionary of numpy arrays
    """
    for i in range(len(d)):
        d[i]["average"] = (d[i]["linksToLines"] + d[i]["linksToTrans"]) / 2
        d[i]["difference"] = d[i]["linksToLines"] - d[i]["linksToTrans"]
    return d


df1 = pd.DataFrame(summarystats(distribution(sourceTextDict, targetTextDict)))
df2 = pd.DataFrame(summarystats(distribution(targetTextDict, sourceTextDict)))

# print(df1)
# print(df2)

df1.to_json('static/latin.js')
df2.to_json('static/english.js')
