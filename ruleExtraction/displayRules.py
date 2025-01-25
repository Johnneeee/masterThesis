import extractHornRulesFunctions
import csv


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

def concatResults(writeTo, iterations):
    filesToConcat = [f"{writeTo}_i{iterations}_r{n}" for n in range(10)]
    storeCountHornRules(f"{writeTo}_i{iterations}_TotalCount",filesToConcat)
    storeTotalMetadata(f"{writeTo}_i{iterations}_TotalCount",filesToConcat)

# concatResults("xlmRBase", 100)
# concatResults("xlmRLarge", 100)
# concatResults("mBertUncased", 100)
# concatResults("mBertCased", 100)
# concatResults("nbBertBase", 100)
# concatResults("nbBertLarge", 100)
# concatResults("norbert", 100)
# concatResults("norbert2", 100)