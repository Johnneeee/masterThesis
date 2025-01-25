import numpy as np
from itertools import combinations
from sympy import symbols
import csv
import datetime

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
    with open(f"output_data/metadata/{writeTo}.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        totalRuntime = [["-", "-", "-", "-", str(datetime.timedelta(seconds=int(sum([float(x[3]) for x in metadata]))))]]
        writer.writerows([["ITERATION", "LEN(HYP)", "SAMPLENR", "RUNTIME(sample)", "RUNTIME(total)"]]) #header
        writer.writerows(metadata)
        writer.writerows(totalRuntime)

def storeHornRules(writeTo, h, lookupTable):
    hornRuleSentences = rulesToSentences(h,lookupTable)
    with open(f"output_data/runsRaw/{writeTo}.csv", 'w', newline='',encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["EXTRACTED HORN RULES"])
        writer.writerows(hornRuleSentences)

# filter
def dropFalseRules(hornRuleSentences):
    negatedRules = [x[0][:-11] for x in hornRuleSentences if x[0][-11:] == " ---> FALSE"]
    rulesFiltered = [x for x in hornRuleSentences if (x[0][-5:] == "FALSE") or (x[0].split(" ---> ")[0]) not in negatedRules]
    return rulesFiltered

def storeHornRulesFiltered(writeTo, h, lookupTable, background):
    hNoBackgorund = set(filter(lambda x: x not in background,h)) # drops background
    hornRuleSentences = rulesToSentences(hNoBackgorund,lookupTable)
    hnofalse = dropFalseRules(hornRuleSentences) # drops false -> x
    with open(f"output_data/runsFiltered/{writeTo}.csv", 'w', newline='',encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["EXTRACTED HORN RULES (FILTERED)"])
        writer.writerows(hnofalse)

# concat
def storeCountHornRulesFiltered(writeTo, fileNames):
    n = len(fileNames)
    hornRulesFiltered = {}
    for fn in fileNames:
        with open(f"output_data/runsFiltered/{fn}.csv", mode = "r",encoding="UTF-8") as file:
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
    with open(f"output_data/runsFilteredTotal/{writeTo}.csv", 'w', newline='',encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["COUNT","EXTRACTED HORN RULES (FILTERED)"])
        writer.writerows(l2)

def storeTotalMetadata(writeTo, fileNames):
    runTimes = []
    for fn in fileNames[:1]:
        rt = 0
        with open(f"output_data/metadata/{fn}.csv", mode = "r",encoding="UTF-8") as file:
            csvFile = csv.reader(file, delimiter=";")
            next(csvFile)
            for line in csvFile:
                print(line[2])
                break
        runTimes.append([fn, round(rt,3)])

    with open(f"output_data/{writeTo}_metadataTotal.csv", 'w', newline='',encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["fileName","runTimes"])
        writer.writerows(runTimes)
