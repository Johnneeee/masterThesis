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
    with open('input_data/background.csv', 'w', newline = '', encoding="UTF-8") as csvfile:
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
                    ruleSentences.append([f"not ({lookupTable[int(rule[2:])]})"])
                else:
                    statementsSentences = " & ".join(list(map(lambda x: lookupTable[int(x[1:])],statements)))
                    ruleSentences.append([f"not ({statementsSentences})"])
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

def dropFalseRules(hornRuleSentences):
    negatedRules = list(filter(lambda x: x[0][:3] == "not",hornRuleSentences)) # get rules that starts with "not"
    rulesFiltered = list(filter(lambda x: [f"not ({x[0].split(' ---> ')[0]})"] not in negatedRules, hornRuleSentences)) # drops false -> x
    return rulesFiltered

def storeMetadata(writeTo, metadata):
    with open(f"output_data/singleRuns/{writeTo}_metadata.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerows([["ITERATION", "LEN(HYP)", "SAMPLENR", "RUNTIME"]]) #header
        writer.writerows(metadata)

def storeHornRules(writeTo, h, lookupTable):
    hornRuleSentences = rulesToSentences(h,lookupTable)
    with open(f"output_data/singleRuns/{writeTo}_HornRules.csv", 'w', newline='',encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["EXTRACTED HORN RULES"])
        writer.writerows(hornRuleSentences)

def storeHornRulesFiltered(writeTo, h, background, lookupTable):
    hNoBackgorund = set(filter(lambda x: x not in background,h)) # filter out background
    hornRuleSentences = rulesToSentences(hNoBackgorund,lookupTable)
    hNoFalseRules = dropFalseRules(hornRuleSentences)   # filter out false rules ie, no false -> x
    with open(f"output_data/singleRuns/{writeTo}_HornRulesFiltered.csv", 'w', newline='',encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["EXTRACTED HORN RULES (FILTERED)"])
        writer.writerows(hNoFalseRules)

def storeCountHornRules(writeTo, fileNames):
    n = len(fileNames)
    hornRules = {}
    for fn in fileNames:
        with open(f"output_data/singleRuns/{fn}_HornRules.csv", mode = "r",encoding="UTF-8") as file:
            csvFile = csv.reader(file, delimiter=";")
            next(csvFile)
            for line in csvFile:
                rule = line[0]
                try:
                    hornRules[rule] += 1
                except:
                    hornRules[rule] = 1
    l = []
    for x in hornRules.items():
        l.append([f"{x[1]}/{n}", x[0]])
    l.sort(key=lambda x: int(x[0][0]),reverse=True) #sorting on count desc
    with open(f"output_data/{writeTo}_HornRulesTotal.csv", 'w', newline='',encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["COUNT","EXTRACTED HORN RULES"])
        writer.writerows(l)

def storeCountHornRulesFiltered(writeTo, fileNames):
    n = len(fileNames)
    hornRulesFiltered = {}
    for fn in fileNames:
        with open(f"output_data/singleRuns/{fn}_HornRulesFiltered.csv", mode = "r",encoding="UTF-8") as file:
            csvFile = csv.reader(file, delimiter=";")
            next(csvFile)
            for line in csvFile:
                rule = line[0]
                try:
                    hornRulesFiltered[rule] += 1
                except:
                    hornRulesFiltered[rule] = 1
    l2 = []
    for x in hornRulesFiltered.items():
        l2.append([f"{x[1]}/{n}", x[0]])
    l2.sort(key=lambda x: int(x[0][0]),reverse=True) #sorting on count desc
    with open(f"output_data/{writeTo}_HornRulesFilteredTotal.csv", 'w', newline='',encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["COUNT","EXTRACTED HORN RULES (FILTERED)"])
        writer.writerows(l2)

def storeTotalMetadata(writeTo, fileNames):
    n = len(fileNames)
    runTimes = []
    for fn in fileNames[:1]:
        rt = 0
        with open(f"output_data/singleRuns/{fn}_metadata.csv", mode = "r",encoding="UTF-8") as file:
            csvFile = csv.reader(file, delimiter=";")
            next(csvFile)
            for line in csvFile:
                print(line[2])
                break
                # rt += float(line[0][3])
        runTimes.append([fn, round(rt,3)])

    with open(f"output_data/{writeTo}_metadataTotal.csv", 'w', newline='',encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["fileName","runTimes"])
        writer.writerows(runTimes)
