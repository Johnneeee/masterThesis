import csv

def totalAvgPPBS(files): #total
    # getting gold data
    with open(f"../censusData/preparedData/utdanningnoLikestilling2023_prepared.csv", mode ='r', encoding="UTF-8") as f:
        csvFile = csv.reader(f, delimiter=";")
        next(csvFile)
        gold_data = {x[0]: float(x[3]) for x in csvFile}

    # calculating avg ppbs across all files
    nrLms = len(files)
    totalAvgPPBS = {}
    for file in files: # adding all ppbs
        with open(f"data/raw/{file}_ppbs.csv", mode ='r', encoding="UTF-8") as f:
            csvFile = csv.reader(f, delimiter=";")
            next(csvFile)
            for occ,gold,pred in csvFile:
                try:
                    totalAvgPPBS[occ] += float(pred)
                except:
                    totalAvgPPBS[occ] = float(pred)
    for x in totalAvgPPBS: # averaging down
        totalAvgPPBS[x] = round(totalAvgPPBS[x] / nrLms, 3)

    head = [["ATTRIBUTE", "GOLD", "PRED"]]
    data = list(map(lambda x: [x, gold_data[x],totalAvgPPBS[x]], gold_data))

    # write data
    with open("data/total/total_ppbs.csv", 'w', newline='', encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerows(head)
        writer.writerows(data)


lms = ["xlmRBase", "xlmRLarge", "mBertUncased", "mBertCased", "nbBertBase", "nbBertLarge", "norbert", "norbert"]
totalAvgPPBS(lms)
