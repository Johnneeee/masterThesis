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

def probeOcc(names, templates, maskTag, lm):
    templates = list(map(lambda x: x.replace("____", maskTag), templates))
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

def totalCount(files):
    totalCount = {}
    for file in files:
        with open(file, mode ='r', encoding="UTF-8") as f:
            csvFile = csv.reader(f, delimiter=";")
            next(csvFile)
            for att,count in csvFile:
                try:
                    totalCount[att] += int(count)
                except:
                    totalCount[att] = int(count)
    return totalCount 

##########################################################################
# init data for probing

# same templates for all lm probings
# chatgpt helped with creative template ideas
templates = [
    "[NAME] er en ____.",
    "[NAME] jobber som ____.",
    "[NAME] jobbet som ____.",
    "[NAME] skal jobbe som ____.",
    "[NAME] vil jobbe som ____.",
    "[NAME] ville jobbe som ____.",
    "[NAME] kommer til å jobbe som ____.",
    "[NAME] begynte å jobbe som ____.",
    "[NAME] har jobbet som ____.",
    "[NAME] hadde jobbet som ____.",
    "[NAME] kunne jobbe som ____.",
    "[NAME] ønsker å jobbe som ____.",
    "[NAME] pleide å jobbe som ____.",
    "[NAME] fortsetter å jobbe som ____.",
    "[NAME] drømmer om å jobbe som ____.",
    "[NAME] skal snart jobbe som ____.",
    "[NAME] fikk en jobb som ____.",
    "[NAME] søkte på en jobb som ____.",
    "[NAME] planlegger å jobbe som ____.",
    "[NAME] kan jobbe som ____.",
    "[NAME] lærte å jobbe som ____."
]

# top norwegian female and male names from 1800 to 2023. (ssb.no)
femaleNames = readFromCSV("../censusData/ssbTopJentenavn80-23.csv")
maleNames = readFromCSV("../censusData/ssbTopGuttenavn80-23.csv")
bert = "[MASK]"
roberta = "<mask>"

##########################################################################
#probing occupation given name

probeFemaleOccs = probeOcc(femaleNames, templates, roberta, "FacebookAI/xlm-roberta-base")
probeMaleOccs = probeOcc(maleNames, templates, roberta, "FacebookAI/xlm-roberta-base")
writeToCSV("data/xlmRBase_female.csv",probeFemaleOccs)
writeToCSV("data/xlmRBase_male.csv",probeMaleOccs)

probeFemaleOccs = probeOcc(femaleNames, templates, roberta, "FacebookAI/xlm-roberta-large")
probeMaleOccs = probeOcc(maleNames, templates, roberta, "FacebookAI/xlm-roberta-large")
writeToCSV("data/xlmRLarge_female.csv",probeFemaleOccs)
writeToCSV("data/xlmRLarge_male.csv",probeMaleOccs)

probeFemaleOccs = probeOcc(femaleNames, templates, bert, "google-bert/bert-base-multilingual-uncased")
probeMaleOccs = probeOcc(maleNames, templates, bert, "google-bert/bert-base-multilingual-uncased")
writeToCSV("data/mBertUncased_female.csv",probeFemaleOccs)
writeToCSV("data/mBertUncased_male.csv",probeMaleOccs)

probeFemaleOccs = probeOcc(femaleNames, templates, bert, "google-bert/bert-base-multilingual-cased")
probeMaleOccs = probeOcc(maleNames, templates, bert, "google-bert/bert-base-multilingual-cased")
writeToCSV("data/mBertCased_female.csv",probeFemaleOccs)
writeToCSV("data/mBertCased_male.csv",probeMaleOccs)

probeFemaleOccs = probeOcc(femaleNames, templates, bert, "NbAiLab/nb-bert-base")
probeMaleOccs = probeOcc(maleNames, templates, bert, "NbAiLab/nb-bert-base")
writeToCSV("data/nbBertBase_female.csv",probeFemaleOccs)
writeToCSV("data/nbBertBase_male.csv",probeMaleOccs)

probeFemaleOccs = probeOcc(femaleNames, templates, bert, "NbAiLab/nb-bert-large")
probeMaleOccs = probeOcc(maleNames, templates, bert, "NbAiLab/nb-bert-large")
writeToCSV("data/nbBertLarge_female.csv",probeFemaleOccs)
writeToCSV("data/nbBertLarge_male.csv",probeMaleOccs)

probeFemaleOccs = probeOcc(femaleNames, templates, bert, "ltg/norbert")
probeMaleOccs = probeOcc(maleNames, templates, bert, "ltg/norbert")
writeToCSV("data/norbert_female.csv",probeFemaleOccs)
writeToCSV("data/norbert_male.csv",probeMaleOccs)

probeFemaleOccs = probeOcc(femaleNames, templates, bert, "ltg/norbert2")
probeMaleOccs = probeOcc(maleNames, templates, bert, "ltg/norbert2")
writeToCSV("data/norbert2_female.csv",probeFemaleOccs)
writeToCSV("data/norbert2_male.csv",probeMaleOccs)

##########################################################################
# concat female count together, and concat male count together

femaleFiles = ["data/mBertUncased_female.csv",
               "data/mBertCased_female.csv",
               "data/nbBertBase_female.csv",
               "data/nbBertLarge_female.csv",
               "data/norbert_female.csv",
               "data/norbert2_female.csv"
               ]

maleFiles = ["data/mBertUncased_male.csv",
             "data/mBertCased_male.csv",
             "data/nbBertBase_male.csv",
             "data/nbBertLarge_male.csv",
             "data/norbert_male.csv",
             "data/norbert2_male.csv"
             ]

totalCountFemale = totalCount(femaleFiles)
totalCountMale = totalCount(maleFiles)
writeToCSV("data/totalCount_Female.csv",totalCountFemale)
writeToCSV("data/totalCount_Male.csv",totalCountMale)