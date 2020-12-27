"""
Matches translations; takes the text tables and adds computed fields
"""
import math
import pandas as pd
import textdistance

RESOLUTION = 1  # Percentage of full page to look for the line (1 = 100%)

file1 = open("static/latin.js")
file2 = open("static/english.js")

text1 = pd.read_json(file1)
text2 = pd.read_json(file2)

text1Dict = text1.to_dict()
text2Dict = text2.to_dict()


def similarity(line1, line2):
    """
    return a number
    """
    distance = textdistance.jaccard(line1, line2)
    closeness = 1 - 1 / (1 + math.exp(-30 * (distance - 0.5)))  # Sigmoid mapping (0,1) to (0,1)
    return closeness


def find_relevant_range(sourcelinenum, sourcedoc, targetdoc):
    """
    This accounts for the shift and stretch, and acts as a coarse prior on where we think the relevant lines are
    """
    center = round(sourcelinenum/len(sourcedoc)*len(targetdoc))
    span = round(len(targetdoc)*RESOLUTION)
    return max(center - span, 0), min(center + span, len(targetdoc))


def compute_confidence(d1, d2):
    """
    "matchIndex" records absref of target lines
    "linksToOther" similarity between self translation and target lines
    "linksFromOther" similarity between self and target line translations
    """
    for i in range(len(d1)):
        minindex, maxindex = find_relevant_range(i, d1, d2)
        d1[i]["matchIndex"] = [(j+1) for j in range(minindex, maxindex)]
        d1[i]["linksToOther"] = [similarity(d1[i]["translation"], d2[j]["line"]) for j in range(minindex, maxindex)]
        d1[i]["linksFromOther"] = [similarity(d1[i]["line"], d2[j]["translation"]) for j in range(minindex, maxindex)]
    return d1


def make_guesses(d):
    """
    compute average and difference of the linkages
    Working on dictionary of numpy arrays
    """
    return d


df1 = pd.DataFrame(make_guesses(compute_confidence(text1Dict, text2Dict)))
df2 = pd.DataFrame(make_guesses(compute_confidence(text2Dict, text1Dict)))

print(df1)
print(df2)

df1.to_json('static/latin.js')
df2.to_json('static/english.js')
