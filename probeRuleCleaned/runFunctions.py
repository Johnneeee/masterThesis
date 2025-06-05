import numpy as np
from itertools import combinations
from sympy import symbols
import csv

# pre Horn Algorithm methods
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
    with open('input_data/backgroundRules.csv', 'w', newline = '', encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows([["BACKGROUND"]])

        writer.writerows(backgroundSentences)

# post Horn Algorithm methods
def rulesToSentences(rules, lookupTable):
    strRules = list(map(lambda x: str(x),rules)) # symbol rules to string rules
    ruleSentences = []
    for rule in strRules:
        # print(rule)
        match rule[0]: # matching on the first letter in string
            case "I": # Case implication                                                        # rule = Implies(v10 & v20 & v23 & v28 & v5, v19)
                antRules = rule[8:-1].split(", ")[0].split(" & ")                               # [v10, v20, v23, v28, v5]
                conRule = rule[8:-1].split(", ")[1]                                             # [v11]
                antSentence = " & ".join(list(map(lambda x: lookupTable[int(x[1:])],antRules))) # mekaniker & Bodø & Afrika & kvinne & eldre enn 60
                conSentence = lookupTable[int(conRule[1:])]                                     # elektriker
                ruleSentence = f"{antSentence} ---> {conSentence}"                              # mekaniker & Bodø & Afrika & kvinne & eldre enn 60 ---> elektriker
                ruleSentences.append([ruleSentence])
            case "~": #case negation
                statements = rule[2:-1].split(" & ")
                if len(statements) == 1: # if the negation clause only contains one value
                    ruleSentences.append([f"{lookupTable[int(rule[2:])]} ---> FALSE"])
                else:
                    statementsSentences = " & ".join(list(map(lambda x: lookupTable[int(x[1:])],statements)))
                    ruleSentences.append([f"{statementsSentences} ---> FALSE"])
            case "F": # False
                ruleSentences.append(["False"])
            case "T": # True
                ruleSentences.append(["True"])
            case "v": # single rule
                ruleSentences.append([lookupTable[int(rule[1:])]])
            case default: #case true????????
                ruleSentences.append([f"default = {rule}"])
                # print(f"default = {rule}")
    ruleSentences.sort(key=lambda x: x[0])# sorting
    return ruleSentences

def storeMetadata(writeTo, metadata):
    with open(f"output_data/metadataRaw/{writeTo}.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerows([["ITERATION", "LEN(HYP)", "SAMPLENR", "RUNTIME(sample)"]]) #header
        writer.writerows(metadata)

def storeHornRules(writeTo, h, lookupTable):
    hornRuleSentences = rulesToSentences(h,lookupTable)
    with open(f"output_data/runsRaw/{writeTo}.csv", 'w', newline='',encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["EXTRACTED HORN RULES"])
        writer.writerows(hornRuleSentences)
