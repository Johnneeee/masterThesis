import numpy as np
from itertools import combinations
from sympy import symbols
import csv

# pre Horn Algorithm
def define_variables(number):
    s = "".join(['v'+str(i)+',' for i in range(number)])
    V = [e for e in symbols(s)]
    return V

def generateBackground(V, attLengths):
    # two values from the same attrutube dimention cant be true simultaneously
    splitIndexes = []
    i = 0
    for x in attLengths:
        i += x
        splitIndexes.append(i)
    splitted = np.split(V, splitIndexes)
    background = set()

    for x in splitted:
        background.update(set(combinations(x, 2)))

    background = set(map(lambda x: ~(x[0] & x[1]),background))

    #storing background
    return background

def storeBackground(background, lookupTable):
    # strBackground = list(map(lambda x: str(x),background))
    backgroundSentences = rulesToSentences(background,lookupTable)
    with open('data/background.csv', 'w', newline = '', encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows([["BACKGROUND"]])

        writer.writerows(backgroundSentences)


# post Horn Algorithm
def storeMetadata(writeTo, metadata):
    with open("rule_extraction/" + writeTo + "_metadata_" + ".csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows([["ITERATION", "HYP LEN", "SAMPLENR", "RUNTIME"]]) #header
        writer.writerows(metadata)


def rulesToSentences(rules, lookupTable):
    strRules = list(map(lambda x: str(x),rules)) # symbol rules to string rules
    print(strRules)
    ruleSentences = []
    for rule in strRules:
        match rule[0]:
            case "I": # Case implication                                                        # rule = Implies(v10 & v20 & v23 & v28 & v5, v19)
                antRules = rule[8:-1].split(", ")[0].split(" & ")                               # [v10, v20, v23, v28, v5]
                conRule = rule[8:-1].split(", ")[1]                                             # [v11]
                antSentence = " & ".join(list(map(lambda x: lookupTable[int(x[1:])],antRules))) # mekaniker & Bodø & Afrika & kvinne & eldre enn 60
                conSentence = lookupTable[int(conRule[1:])]                                     # elektriker
                ruleSentence = f"{antSentence} ---> {conSentence}"                              # mekaniker & Bodø & Afrika & kvinne & eldre enn 60 ---> elektriker
                ruleSentences.append([ruleSentence])
            case "~": #case negation
                statements = rule[2:-1].split(" & ")
                statementsSentences = " & ".join(list(map(lambda x: lookupTable[int(x[1:])],statements)))
                ruleSentences.append([f"not ({statementsSentences})"])
            case "v": #case true????????
                print(f"Sta {rule}")
            case "len1 true": 
                pass
            case "len1 neg":
                pass
    return ruleSentences

def dropFalseRules(hornRuleSentences):
    negatedRules = list(filter(lambda x: x[0][:3] == "not",hornRuleSentences)) # get rules that starts with "not"
    rulesFiltered = list(filter(lambda x: [f"not ({x[0].split(' --->')[0]})"] not in negatedRules, hornRuleSentences)) # drops false -> x
    return rulesFiltered

def storeHornRules(writeTo, h, background,lookupTable):
    # filterH = list(filter(lambda x: x not in background,h)) # filter out background
    # strH = list(map(lambda x: str(x),h))
    hornRuleSentences = rulesToSentences(h,lookupTable)
    # filteredSentences = dropFalseRules(hornRuleSentences)   # filter out false rules
    with open("rule_extraction/" + writeTo + "_HornRules_" + ".csv", 'w', newline='',encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["EXTRACTED HORN RULES"])
        writer.writerows(hornRuleSentences)
    # for x in formatedRules:
    #     print(x)