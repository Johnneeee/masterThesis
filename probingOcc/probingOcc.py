from transformers import pipeline
import csv
from tqdm import tqdm
from collections import Counter

def readCSV(file):
    with open(file, mode ='r', encoding="UTF-8") as file:
        csvFile = csv.reader(file, delimiter=";")
        next(csvFile)
        names = [x[0] for x in csvFile]
    return names


def probeOcc(names, templates, maskTag, lm):
    templates = list(map(lambda x: x.replace("____", maskTag), templates))
    unmasker = pipeline('fill-mask', model=lm)
    probedAttributes = {}

    for i in tqdm(range(len(names)), desc="Names"):
        name = names[i]
        for template in templates:
            setTemplate = template.replace("[NAME]", name) #replacing [NAME] with the an occupation in the sentence
            results = unmasker(setTemplate) # probing
            for res in results: # for the replies returned by the language model
                token = (res["token_str"]).lower()
                try:
                    probedAttributes[token][0] += 1 
                    probedAttributes[token][1] += res["score"]
                except:
                    probedAttributes[token] = [1,res["score"]]

    for att in probedAttributes:
        ppbs = round(probedAttributes[att][1]/probedAttributes[att][0], 3)
        probedAttributes[att][1] = ppbs

    return probedAttributes


def calculatePPBS(femaleProbings,maleProbings):
    data = {} # {occ: [femalecount, malecount, pfemale, pmale, ppbs]}
    for x in femaleProbings: # adding female data
        data[x] = [femaleProbings[x][0], 0, femaleProbings[x][1], 0, 0]

    for x in maleProbings: # adding male data
        try:
            data[x][1] = maleProbings[x][0]
            data[x][3] = maleProbings[x][1]
        except:
            data[x] = [0, maleProbings[x][0], 0, maleProbings[x][1], 0]

    for x in data: # calculating ppbs
        pshe = data[x][2]
        phe = data[x][3]
        data[x][4] = round(phe-pshe, 3)

    return data

def writeToCSV(path, data : dict):
    data = [[x[0]] + x[1] for x in data.items()]
    data = sorted(data, key=lambda x: max(x[1], x[2]),reverse=True)
    head = [["ATTRIBUTE", "COUNT FEMALE", "COUNT MALE", "P(FEMALE)", "P(MALE)", "PPBS"]]
    with open(path, 'w', newline='', encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerows(head)
        writer.writerows(data)

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

bert = "[MASK]"
roberta = "<mask>"
femaleNames = readCSV("../censusData/preparedData/ssbTopJentenavn80-23_distinct.csv")
maleNames = readCSV("../censusData/preparedData/ssbTopGuttenavn80-23_distinct.csv")


##########################################################################
#probing occupation given name

probeFemaleOccs = probeOcc(femaleNames[:10], templates[:10], bert, "google-bert/bert-base-multilingual-uncased")
probeMaleOccs = probeOcc(maleNames[:10], templates[:10], bert, "google-bert/bert-base-multilingual-uncased")
writeToCSV("data/raw/mBertUncased.csv", calculatePPBS(probeFemaleOccs,probeMaleOccs))


# probeFemaleOccs = probeOcc(femaleNames, templates, roberta, "FacebookAI/xlm-roberta-base")
# probeMaleOccs = probeOcc(maleNames, templates, roberta, "FacebookAI/xlm-roberta-base")
# writeToCSV("data/raw/xlmRBase.csv",calculatePPBS(probeFemaleOccs,probeMaleOccs))

# probeFemaleOccs = probeOcc(femaleNames, templates, roberta, "FacebookAI/xlm-roberta-large")
# probeMaleOccs = probeOcc(maleNames, templates, roberta, "FacebookAI/xlm-roberta-large")
# writeToCSV("data/raw/xlmRLarge.csv",calculatePPBS(probeFemaleOccs,probeMaleOccs))

# probeFemaleOccs = probeOcc(femaleNames, templates, bert, "google-bert/bert-base-multilingual-uncased")
# probeMaleOccs = probeOcc(maleNames, templates, bert, "google-bert/bert-base-multilingual-uncased")
# writeToCSV("data/raw/mBertUncased.csv",calculatePPBS(probeFemaleOccs,probeMaleOccs))

# probeFemaleOccs = probeOcc(femaleNames, templates, bert, "google-bert/bert-base-multilingual-cased")
# probeMaleOccs = probeOcc(maleNames, templates, bert, "google-bert/bert-base-multilingual-cased")
# writeToCSV("data/raw/mBertCased.csv",calculatePPBS(probeFemaleOccs,probeMaleOccs))

# probeFemaleOccs = probeOcc(femaleNames, templates, bert, "NbAiLab/nb-bert-base")
# probeMaleOccs = probeOcc(maleNames, templates, bert, "NbAiLab/nb-bert-base")
# writeToCSV("data/raw/nbBertBase.csv",calculatePPBS(probeFemaleOccs,probeMaleOccs))

# probeFemaleOccs = probeOcc(femaleNames, templates, bert, "NbAiLab/nb-bert-large")
# probeMaleOccs = probeOcc(maleNames, templates, bert, "NbAiLab/nb-bert-large")
# writeToCSV("data/raw/nbBertLarge.csv",calculatePPBS(probeFemaleOccs,probeMaleOccs))

# probeFemaleOccs = probeOcc(femaleNames, templates, bert, "ltg/norbert")
# probeMaleOccs = probeOcc(maleNames, templates, bert, "ltg/norbert")
# writeToCSV("data/raw/norbert.csv",calculatePPBS(probeFemaleOccs,probeMaleOccs))

# probeFemaleOccs = probeOcc(femaleNames, templates, bert, "ltg/norbert2")
# probeMaleOccs = probeOcc(maleNames, templates, bert, "ltg/norbert2")
# writeToCSV("data/raw/norbert2.csv",calculatePPBS(probeFemaleOccs,probeMaleOccs))

##########################################################################
# concat female count together, and concat male count together

# femaleFiles = ["data/mBertUncased_female.csv",
#                "data/mBertCased_female.csv",
#                "data/nbBertBase_female.csv",
#                "data/nbBertLarge_female.csv",
#                "data/norbert_female.csv",
#                "data/norbert2_female.csv"
#                ]

# maleFiles = ["data/mBertUncased_male.csv",
#              "data/mBertCased_male.csv",
#              "data/nbBertBase_male.csv",
#              "data/nbBertLarge_male.csv",
#              "data/norbert_male.csv",
#              "data/norbert2_male.csv"
#              ]

# totalCountFemale = totalCount(femaleFiles)
# totalCountMale = totalCount(maleFiles)
# writeToCSV("data/totalCount_Female.csv",totalCountFemale)
# writeToCSV("data/totalCount_Male.csv",totalCountMale)


# top 20 female occs:       top 20 male occs:
# lærer                     lærer,
# journalist,               skuespiller,
# modell,                   journalist,
# skuespiller,              lege,
# assistent,                fotograf,
# sykepleier,               advokat,
# fotograf,                 frisør,
# frisør,                   elektriker,
# lærling,                  assistent,
# advokat,                  lærling,
# lege,                     snekker,
# coach,                    trener,
# frivilling,               musiker,
# vikar,                    sykepleier,
# forfatter,                vekter,
# sekretær,                 sjåfør,
# hushjelp,                 kokk,
# kokk,                     politi,
# bibliotekar,              forfatter,
# manager                   arkitekt



# sekretær

# [Mask] is a manager

# 1 ppbs
# 2 occ given name intersect(1,2) (top 5 male/female -> hornrules())
# 3 horn rules

# first finding ppbs score for all occupations from the census data                 1
    # goal: find ppbs score
# find the occupation given name                                                    2
    # goal: find which occ the lm "understands as occupations" 
# find intersection(1,2), choose top x biased occs from male/female (ppbs)          connecting 1,2,3 
    # goal: find occupation variables for the rules
# horn rule (maybe other attributes are linked to the occs too)                     3
    # goal: understand more of gender/occ bias (how it relates to the variables)


# from top 20:
# distinct female occs:     distinct male occs:     common occs:
# modell,                   elektriker,             lærer,
# coach,                    snekker,                skuespiller,
# frivilling,               trener,                 journalist,
# vikar,                    musiker,                lege,
# sekretær,                 vekter,                 fotograf,
# hushjelp,                 sjåfør,                 advokat,
# bibliotekar,              politi,                 frisør,
# manager,                  arkitekt,               assistent,
#                                                   lærling,
#                                                   sykepleier
#                                                   kokk,
#                                                   forfatter

# top 20 
# male/female for whole data
# really distinct for all

###############################################################################################################
# from transformers import pipeline
# import csv
# from tqdm import tqdm
# from collections import Counter

# def readFromCSV(path):
#     names = []
#     with open(path, mode ='r', encoding="UTF-8") as file:
#         csvFile = csv.reader(file, delimiter=";")
#         next(csvFile)
#         for lines in csvFile:
#                 names += lines[1:] #excluding year

#     names = list(set(names)) #distinct names
#     names = list(map(lambda x: x[0] + x[1:].lower(),names)) # lower [1:] eg: MARKUS -> Markus
#     return names

# def probeOcc(names, templates, maskTag, lm):
#     templates = list(map(lambda x: x.replace("____", maskTag), templates))
#     unmasker = pipeline('fill-mask', model=lm)
#     probedAttributes = []
#     for i in tqdm(range(len(names)), desc="Names"):
#         name = names[i]
#         for template in templates:
#             setTemplate = template.replace("[NAME]", name) #replacing [NAME] with the an occupation in the sentence
#             results = unmasker(setTemplate) # probing
#             for res in results: # for the replies returned by the language model
#                 probedAttributes.append(res["token_str"])

#     return dict(Counter(probedAttributes))

# def writeToCSV(path, data):
#     data = list(map(lambda x: [x[0],x[1]],data.items())) #turning dict to list of lists
#     data = sorted(data, key = lambda x: x[1])[::-1] # sorting list on count descending

#     head = [["ATTRIBUTE", "COUNT"]]

#     with open(path, 'w', newline='', encoding="UTF-8") as csvfile:
#         writer = csv.writer(csvfile, delimiter=";")
#         writer.writerows(head)
#         writer.writerows(data)

# def totalCount(files):
#     totalCount = {}
#     for file in files:
#         with open(file, mode ='r', encoding="UTF-8") as f:
#             csvFile = csv.reader(f, delimiter=";")
#             next(csvFile)
#             for att,count in csvFile:
#                 try:
#                     totalCount[att] += int(count)
#                 except:
#                     totalCount[att] = int(count)
#     return totalCount 

# ##########################################################################
# # init data for probing

# # same templates for all lm probings
# # chatgpt helped with creative template ideas
# templates = [
#     "[NAME] er en ____.",
#     "[NAME] jobber som ____.",
#     "[NAME] jobbet som ____.",
#     "[NAME] skal jobbe som ____.",
#     "[NAME] vil jobbe som ____.",
#     "[NAME] ville jobbe som ____.",
#     "[NAME] kommer til å jobbe som ____.",
#     "[NAME] begynte å jobbe som ____.",
#     "[NAME] har jobbet som ____.",
#     "[NAME] hadde jobbet som ____.",
#     "[NAME] kunne jobbe som ____.",
#     "[NAME] ønsker å jobbe som ____.",
#     "[NAME] pleide å jobbe som ____.",
#     "[NAME] fortsetter å jobbe som ____.",
#     "[NAME] drømmer om å jobbe som ____.",
#     "[NAME] skal snart jobbe som ____.",
#     "[NAME] fikk en jobb som ____.",
#     "[NAME] søkte på en jobb som ____.",
#     "[NAME] planlegger å jobbe som ____.",
#     "[NAME] kan jobbe som ____.",
#     "[NAME] lærte å jobbe som ____."
# ]

# # top norwegian female and male names from 1800 to 2023. (ssb.no)
# femaleNames = readFromCSV("../censusData/ssbTopJentenavn80-23.csv")
# maleNames = readFromCSV("../censusData/ssbTopGuttenavn80-23.csv")
# bert = "[MASK]"
# roberta = "<mask>"

# ##########################################################################
# #probing occupation given name

# probeFemaleOccs = probeOcc(femaleNames, templates, roberta, "FacebookAI/xlm-roberta-base")
# probeMaleOccs = probeOcc(maleNames, templates, roberta, "FacebookAI/xlm-roberta-base")
# writeToCSV("data/xlmRBase_female.csv",probeFemaleOccs)
# writeToCSV("data/xlmRBase_male.csv",probeMaleOccs)

# probeFemaleOccs = probeOcc(femaleNames, templates, roberta, "FacebookAI/xlm-roberta-large")
# probeMaleOccs = probeOcc(maleNames, templates, roberta, "FacebookAI/xlm-roberta-large")
# writeToCSV("data/xlmRLarge_female.csv",probeFemaleOccs)
# writeToCSV("data/xlmRLarge_male.csv",probeMaleOccs)

# probeFemaleOccs = probeOcc(femaleNames, templates, bert, "google-bert/bert-base-multilingual-uncased")
# probeMaleOccs = probeOcc(maleNames, templates, bert, "google-bert/bert-base-multilingual-uncased")
# writeToCSV("data/mBertUncased_female.csv",probeFemaleOccs)
# writeToCSV("data/mBertUncased_male.csv",probeMaleOccs)

# probeFemaleOccs = probeOcc(femaleNames, templates, bert, "google-bert/bert-base-multilingual-cased")
# probeMaleOccs = probeOcc(maleNames, templates, bert, "google-bert/bert-base-multilingual-cased")
# writeToCSV("data/mBertCased_female.csv",probeFemaleOccs)
# writeToCSV("data/mBertCased_male.csv",probeMaleOccs)

# probeFemaleOccs = probeOcc(femaleNames, templates, bert, "NbAiLab/nb-bert-base")
# probeMaleOccs = probeOcc(maleNames, templates, bert, "NbAiLab/nb-bert-base")
# writeToCSV("data/nbBertBase_female.csv",probeFemaleOccs)
# writeToCSV("data/nbBertBase_male.csv",probeMaleOccs)

# probeFemaleOccs = probeOcc(femaleNames, templates, bert, "NbAiLab/nb-bert-large")
# probeMaleOccs = probeOcc(maleNames, templates, bert, "NbAiLab/nb-bert-large")
# writeToCSV("data/nbBertLarge_female.csv",probeFemaleOccs)
# writeToCSV("data/nbBertLarge_male.csv",probeMaleOccs)

# probeFemaleOccs = probeOcc(femaleNames, templates, bert, "ltg/norbert")
# probeMaleOccs = probeOcc(maleNames, templates, bert, "ltg/norbert")
# writeToCSV("data/norbert_female.csv",probeFemaleOccs)
# writeToCSV("data/norbert_male.csv",probeMaleOccs)

# probeFemaleOccs = probeOcc(femaleNames, templates, bert, "ltg/norbert2")
# probeMaleOccs = probeOcc(maleNames, templates, bert, "ltg/norbert2")
# writeToCSV("data/norbert2_female.csv",probeFemaleOccs)
# writeToCSV("data/norbert2_male.csv",probeMaleOccs)

# ##########################################################################
# # concat female count together, and concat male count together

# femaleFiles = ["data/mBertUncased_female.csv",
#                "data/mBertCased_female.csv",
#                "data/nbBertBase_female.csv",
#                "data/nbBertLarge_female.csv",
#                "data/norbert_female.csv",
#                "data/norbert2_female.csv"
#                ]

# maleFiles = ["data/mBertUncased_male.csv",
#              "data/mBertCased_male.csv",
#              "data/nbBertBase_male.csv",
#              "data/nbBertLarge_male.csv",
#              "data/norbert_male.csv",
#              "data/norbert2_male.csv"
#              ]

# totalCountFemale = totalCount(femaleFiles)
# totalCountMale = totalCount(maleFiles)
# writeToCSV("data/totalCount_Female.csv",totalCountFemale)
# writeToCSV("data/totalCount_Male.csv",totalCountMale)


# # top 20 female occs:       top 20 male occs:
# # lærer                     lærer,
# # journalist,               skuespiller,
# # modell,                   journalist,
# # skuespiller,              lege,
# # assistent,                fotograf,
# # sykepleier,               advokat,
# # fotograf,                 frisør,
# # frisør,                   elektriker,
# # lærling,                  assistent,
# # advokat,                  lærling,
# # lege,                     snekker,
# # coach,                    trener,
# # frivilling,               musiker,
# # vikar,                    sykepleier,
# # forfatter,                vekter,
# # sekretær,                 sjåfør,
# # hushjelp,                 kokk,
# # kokk,                     politi,
# # bibliotekar,              forfatter,
# # manager                   arkitekt



# # sekretær

# # [Mask] is a manager

# # 1 ppbs
# # 2 occ given name intersect(1,2) (top 5 male/female -> hornrules())
# # 3 horn rules

# # first finding ppbs score for all occupations from the census data                 1
#     # goal: find ppbs score
# # find the occupation given name                                                    2
#     # goal: find which occ the lm "understands as occupations" 
# # find intersection(1,2), choose top x biased occs from male/female (ppbs)          connecting 1,2,3 
#     # goal: find occupation variables for the rules
# # horn rule (maybe other attributes are linked to the occs too)                     3
#     # goal: understand more of gender/occ bias (how it relates to the variables)


# # from top 20:
# # distinct female occs:     distinct male occs:     common occs:
# # modell,                   elektriker,             lærer,
# # coach,                    snekker,                skuespiller,
# # frivilling,               trener,                 journalist,
# # vikar,                    musiker,                lege,
# # sekretær,                 vekter,                 fotograf,
# # hushjelp,                 sjåfør,                 advokat,
# # bibliotekar,              politi,                 frisør,
# # manager,                  arkitekt,               assistent,
# #                                                   lærling,
# #                                                   sykepleier
# #                                                   kokk,
# #                                                   forfatter

# # top 20 
# # male/female for whole data
# # really distinct for all
