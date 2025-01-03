from transformers import pipeline
import csv
from tqdm import tqdm
from collections import Counter

def readFromCSV(path):
    names = []
    with open(path, mode ='r', encoding="UTF-8") as file:
        csvFile = csv.reader(file, delimiter=";")
        next(csvFile)
        for lines in csvFile:
                names += lines[1:] #excluding year

    names = list(set(names)) #distinct names
    names = list(map(lambda x: x[0] + x[1:].lower(),names)) # lower [1:] eg: MARKUS -> Markus
    return names

def probeOcc(names, templates, lm):
    unmasker = pipeline('fill-mask', model=lm)
    probedAttributes = []

    for i in tqdm(range(len(names)), desc="Names"):
        name = names[i]
        for template in templates:
            setTemplate = template.replace("[NAME]", name) #replacing [NAME] with the an occupation in the sentence
            results = unmasker(setTemplate) # probing
            for res in results: # for the replies returned by the language model
                probedAttributes.append(res["token_str"])

    return dict(Counter(probedAttributes))

def writeToCSV(path, data):
    data = list(map(lambda x: [x[0],x[1]],data.items())) #turning dict to list of lists
    data = sorted(data, key = lambda x: x[1])[::-1] # sorting list on count descending

    head = [["ATTRIBUTE", "COUNT"]]

    with open(path, 'w', newline='', encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerows(head)
        writer.writerows(data)

def addToTotal(files):
    totalCount = {}
    for file in files:
        with open(file, mode ='r', encoding="UTF-8") as file:
            csvFile = csv.reader(file, delimiter=";")
            next(csvFile)
            for att,count in csvFile:
                try:
                    totalCount[att] += int(count)
                except:
                    totalCount[att] = int(count)
    return totalCount 

##########################################################################
#probing occupation given names

# same templates for all lm probings
templates = [
    "[NAME] er en [MASK].",
    "[NAME] jobber som [MASK].",
    "[NAME] jobbet som [MASK].",
    "[NAME] skal jobbe som [MASK].",
    "[NAME] vil jobbe som [MASK].",
    "[NAME] ville jobbe som [MASK].",
    "[NAME] kommer til å jobbe som [MASK].",
    "[NAME] begynte å jobbe som [MASK].",
    "[NAME] har jobbet som [MASK].",
    "[NAME] hadde jobbet som [MASK].",
    "[NAME] kunne jobbe som [MASK].",
    "[NAME] ønsker å jobbe som [MASK].",
    "[NAME] pleide å jobbe som [MASK].",
    "[NAME] fortsetter å jobbe som [MASK].",
    "[NAME] drømmer om å jobbe som [MASK].",
    "[NAME] skal snart jobbe som [MASK].",
    "[NAME] fikk en jobb som [MASK].",
    "[NAME] søkte på en jobb som [MASK].",
    "[NAME] planlegger å jobbe som [MASK].",
    "[NAME] kan jobbe som [MASK].",
    "[NAME] lærte å jobbe som [MASK].",
]

# top norwegian female and male names from 1800 to 2023. Data from ssb
femaleNames = readFromCSV("../censusData/ssbTopJentenavn80-23.csv")
maleNames = readFromCSV("../censusData/ssbTopGuttenavn80-23.csv")

probeFemaleOccs = probeOcc(femaleNames, templates, "google-bert/bert-base-multilingual-uncased")
probeMaleOccs = probeOcc(maleNames, templates, "google-bert/bert-base-multilingual-uncased")
writeToCSV("data/bbMultiUncased_female.csv",probeFemaleOccs)
writeToCSV("data/bbMultiUncased_male.csv",probeMaleOccs)

probeFemaleOccs = probeOcc(femaleNames, templates, "google-bert/bert-base-multilingual-cased")
probeMaleOccs = probeOcc(maleNames, templates, "google-bert/bert-base-multilingual-cased")
writeToCSV("data/bbMultiCased_female.csv",probeFemaleOccs)
writeToCSV("data/bbMultiCased_male.csv",probeMaleOccs)

probeFemaleOccs = probeOcc(femaleNames, templates, "NbAiLab/nb-bert-base")
probeMaleOccs = probeOcc(maleNames, templates, "NbAiLab/nb-bert-base")
writeToCSV("data/nbBertBase_female.csv",probeFemaleOccs)
writeToCSV("data/nbBertBase_male.csv",probeMaleOccs)

probeFemaleOccs = probeOcc(femaleNames, templates, "NbAiLab/nb-bert-large")
probeMaleOccs = probeOcc(maleNames, templates, "NbAiLab/nb-bert-large")
writeToCSV("data/nbBertLarge_female.csv",probeFemaleOccs)
writeToCSV("data/nbBertLarge_male.csv",probeMaleOccs)

probeFemaleOccs = probeOcc(femaleNames, templates, "ltg/norbert")
probeMaleOccs = probeOcc(maleNames, templates, "ltg/norbert")
writeToCSV("data/norbert_female.csv",probeFemaleOccs)
writeToCSV("data/norbert_male.csv",probeMaleOccs)

probeFemaleOccs = probeOcc(femaleNames, templates, "ltg/norbert2")
probeMaleOccs = probeOcc(maleNames, templates, "ltg/norbert2")
writeToCSV("data/norbert2_female.csv",probeFemaleOccs)
writeToCSV("data/norbert2_male.csv",probeMaleOccs)

#############################
# concat female count together, and concat male count together

femaleFiles = ["data/bbMultiUncased_female.csv",
               "data/bbMultiCased_female.csv",
               "data/nbBertBase_female.csv",
               "data/nbBertLarge_female.csv",
               "data/norbert_female.csv",
               "data/norbert2_female.csv"
               ]

maleFiles = ["data/bbMultiUncased_male.csv",
             "data/bbMultiCased_male.csv",
             "data/nbBertBase_male.csv",
             "data/nbBertLarge_male.csv",
             "data/norbert_male.csv",
             "data/norbert2_male.csv"
             ]

totalCounterFemale = addToTotal(femaleFiles)
totalCounterMale = addToTotal(maleFiles)

writeToCSV("data/totalCount_Female.csv",totalCounterFemale)
writeToCSV("data/totalCount_Male.csv",totalCounterMale)

# top 10 female occs:       top 10 male occs:       common occs from top 10:
# skuespiller,              lærer,                  lærer,
# lærer,                    journalist,             journalist,
# journalist,               skuespiller,            skuespiller,
# advokat,                  advokat,                advokat,
# frisør,                   fotograf,               assistent?,
# assistent?,               assistent?,             lærling?,
# sykepleier,               lærling?,               frisør,
# lærling?,                 politiker,              fotograf,
# guide?,                   frisør,                 forfatter,
# coach?,                   rørlegger,              sykepleier
# fotograf,                 kokk,
# modell,                   forfatter,
# terapeut,                 sykepleier,
# forfatter                 agent

# from top 10:
# distinct female occs:     distinct male occs:     common occs:
# guide?,                   politiker,              lærer,
# coach?,                   rørlegger,              journalist,
# modell,                   kokk,                   skuespiller,
# terapaut                  agent,                  advokat,
#                                                   assistent?,
#                                                   lærling?,
#                                                   frisør,
#                                                   fotograf,
#                                                   forfatter,
#                                                   sykepleier