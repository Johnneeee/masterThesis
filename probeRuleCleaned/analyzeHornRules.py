import csv

#getting available filenames
# lms = ["xlmRBase", "xlmRLarge", "mBertUncased", "mBertCased", "nbBertBase", "nbBertLarge", "norbert", "norbert2"]
# tags = ["i100_r0","i100_r1","i100_r2","i200_r0","i200_r1","i300_r0"]

allFiles = [
    "xlmRBase_i5_r0",
    "xlmRBase_i5_r1",
    "xlmRBase_i10_r0",
    "mBertUnCased_i5_r0",
    "mBertUnCased_i5_r1",
    "mBertUnCased_i10_r0",
]

# for lm in lms:
#     for tag in tags:
#         allFiles.append(f"{lm}_{tag}")

#####################################################################################################################
# Filter Runs
def filterHornRules(filterFile):
    with open(f"output_data/backgroundRules/backgroundRules.csv", mode = "r",encoding="UTF-8") as file:
        csvFile = csv.reader(file, delimiter=";")
        next(csvFile)
        background = [x for x in csvFile]
    
    with open(f"output_data/hornRules/{filterFile}.csv", mode = "r",encoding="UTF-8") as file:
        csvFile = csv.reader(file, delimiter=";")
        next(csvFile)
        hornRules = [x for x in csvFile]

    hornRules = [x for x in hornRules if x not in background]

    falseRules = []
    for x in hornRules:
        if len(x[0].split(" ---> ")) != 1:
            if x[0].split(" ---> ")[1] == "FALSE":
                falseRules.append(x)

    hornRules = [x for x in hornRules if [f"{x[0].split(' ---> ')[0]} ---> FALSE"] not in falseRules] + falseRules

    with open(f"output_data/hornRulesFiltered/{filterFile}.csv", 'w', newline='',encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["HORN RULES (filtered)"])
        writer.writerows(hornRules)

for file in allFiles:
    filterHornRules(file)

#####################################################################################################################
# adding guiding comments
def addGuide(dataFile):
    with open(f"input_data/ethnicityValues.csv", mode = "r",encoding="UTF-8") as file:
        csvFile = csv.reader(file, delimiter=";")
        next(csvFile)
        ethnicity = [x[0] for x in csvFile]
        # print(ethnicity)

    with open(f"input_data/livingLocValues.csv", mode = "r",encoding="UTF-8") as file:
        csvFile = csv.reader(file, delimiter=";")
        next(csvFile)
        city = [x[0] for x in csvFile]
        # print(city)

    with open(f"output_data/runsFiltered/{dataFile}.csv", mode = "r",encoding="UTF-8") as file:
        csvFile = csv.reader(file, delimiter=";")
        next(csvFile)
        hornRules = [x for x in csvFile]
        # print(hornRules)

    for i in range(len(hornRules)):
        for x in city:
            hornRules[i] = [hornRules[i][0].replace(x,f"{x}(livingLoc)")]
        for x in ethnicity:
            hornRules[i] = [hornRules[i][0].replace(x,f"{x}(ethnicity)")]

    with open(f"output_data/runsFiltered/fake{dataFile}.csv", 'w', newline='',encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["HORN RULES (filtered + guide tags)"])
        writer.writerows(hornRules)

# for file in allFiles:
#     addGuide(file)

#####################################################################################################################
# # Collect horn rules
def collectHornRules(writeTo, files, weights):
    countRules = {}
    for i in range(len(files)):
        with open(f"output_data/hornRulesFiltered/{files[i]}.csv", mode = "r",encoding="UTF-8") as f:
            csvFile = csv.reader(f, delimiter=";")
            next(csvFile)
            for line in csvFile:
                rule = line[0]
                try:
                    countRules[rule] += weights[i]
                except:
                    countRules[rule] = weights[i]
    
    rules = [[f"{x[1]}/{sum(weights)}",x[0]] for x in countRules.items()]
    rules.sort(key=lambda x: int(x[0].split("/")[0]),reverse=True)

    with open(f"output_data/hornRulesFilteredCollected/{writeTo}.csv", 'w', newline='',encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["COUNT","HORN RULES (filtered)"])
        writer.writerows(rules)

eq100 = ["i100_r0","i100_r1","i100_r2"]
eq200 = ["i200_r0","i200_r1"]
eq300 = ["i300_r0"]

collectHornRules("xlmRBase_i5", ["xlmRBase_i5_r0","xlmRBase_i5_r1"], [1,1])
collectHornRules("mBertUncased_i5", ["mBertUncased_i5_r0","mBertUncased_i5_r1"], [1,1])
# for lm in lms:
#     collectHornRules(f"{lm}_i100", [f"{lm}_{x}" for x in eq100], [1,1,1])
#     collectHornRules(f"{lm}_i200", [f"{lm}_{x}" for x in eq200], [1,1])
#     collectHornRules(f"{lm}_i300", [f"{lm}_{x}" for x in eq300], [1])
#     collectHornRules(f"{lm}_iAll(weighted)", [f"{lm}_{x}" for x in eq100 + eq200 + eq300], [1,1,1,2,2,3])
#     collectHornRules(f"{lm}_iAll", [f"{lm}_{x}" for x in eq100 + eq200 + eq300], [1,1,1,1,1,1])