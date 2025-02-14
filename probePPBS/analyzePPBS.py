import csv


def readCSV(path):
    data = []
    with open(path, encoding = "UTF-8") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader) # skip first line which includes the description, ie [occupation, female, male]
        for line in reader:
            occ = line[0].lower()
            she = round(float(line[1])/100, 3) # /100 to turn into percentage
            he = round(float(line[2])/100, 3)
            gold_ppbs = round(he-she,3)
            data.append([occ,she,he,gold_ppbs])
    return data # [[occ,p_she,p_he,gold_ppbs]]


def totalAvgPPBS(files): #total
    nrLms = len(files)
    totalAvgPPBS = {}
    for file in files:
        with open(file, mode ='r', encoding="UTF-8") as f:
            csvFile = csv.reader(f, delimiter=";")
            next(csvFile)
            for occ,gold,pred in csvFile:
                try:
                    totalAvgPPBS[occ] += float(pred)
                except:
                    totalAvgPPBS[occ] = float(pred)
    for x in totalAvgPPBS:
        totalAvgPPBS[x] = round(totalAvgPPBS[x] / nrLms, 3)

    return totalAvgPPBS


def writeCSV(path, gold_data, pred_data):
    data = list(map(lambda x: [x[0],x[3],pred_data[x[0]]],gold_data)) 
    head = [["ATTRIBUTE", "GOLD", "PRED"]]

    with open(path, 'w', newline='', encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerows(head)
        writer.writerows(data)
##########################################################################
# averaging ppbs across all the lms

lms = ["xlmRBase", "xlmRLarge", "mBertUncased", "mBertCased", "nbBertBase", "nbBertLarge", "norbert", "norbert"]

files = [
    "data/xlmRBase_ppbs.csv",
    "data/xlmRLarge_ppbs.csv",
    "data/mBertUncased_ppbs.csv",
    "data/mBertCased_ppbs.csv",
    "data/nbBertBase_ppbs.csv",
    "data/nbBertLarge_ppbs.csv",
    "data/norbert_ppbs.csv",
    "data/norbert2_ppbs.csv"
]

gold_data = readCSV("../censusData/utdanningnoLikestilling2023.csv")
occs = list(map(lambda x: x[0],gold_data))

totalAvgPred = totalAvgPPBS(files)
writeCSV("data/totalAvgPPBS_ppbs.csv", gold_data, totalAvgPred)