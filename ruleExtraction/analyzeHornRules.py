import csv

# Filter Runs
def filterHornRules(filterFile):
    with open(f"input_data/background.csv", mode = "r",encoding="UTF-8") as file:
        csvFile = csv.reader(file, delimiter=";")
        next(csvFile)
        background = [x for x in csvFile]
    
    with open(f"output_data/runsRaw/{filterFile}.csv", mode = "r",encoding="UTF-8") as file:
        csvFile = csv.reader(file, delimiter=";")
        next(csvFile)
        hornRules = [x for x in csvFile]

    hornRules = [x for x in hornRules if x not in background]

    falseRules = [x for x in hornRules if x[0].split(" ---> ")[1] == "FALSE"]
    hornRules = [x for x in hornRules if [f"{x[0].split(' ---> ')[0]} ---> FALSE"] not in falseRules] + falseRules

    with open(f"output_data/runsFiltered/{filterFile}.csv", 'w', newline='',encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["HORN RULES (filtered)"])
        writer.writerows(hornRules)


lms = ["xlmRBase", "xlmRLarge", "mBertUncased", "mBertCased", "nbBertBase", "nbBertLarge", "norbert", "norbert2"]
tags = ["i100_r0","i100_r1","i100_r2","i200_r0","i200_r1","i300_r0"]
allFiles = []

for lm in lms:
    for tag in tags:
        allFiles.append(f"{lm}_{tag}")

# for file in allFiles:
#     filterHornRules(file)

#####################################################################################################################
# # Concat runs
def countRules(writeTo, files, weights):
    countRules = {}
    for i in range(len(files)):
        with open(f"output_data/runsFiltered/{files[i]}.csv", mode = "r",encoding="UTF-8") as f:
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

    with open(f"output_data/runsFilteredTotal/{writeTo}.csv", 'w', newline='',encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["COUNT","HORN RULES (filtered)"])
        writer.writerows(rules)

eq100 = ["i100_r0","i100_r1","i100_r2"]
eq200 = ["i200_r0","i200_r1"]
eq300 = ["i300_r0"]

# for lm in lms:
    # countRules(f"{lm}_i100", [f"{lm}_{x}" for x in eq100], [1,1,1])
    # countRules(f"{lm}_i200", [f"{lm}_{x}" for x in eq200], [1,1])
    # countRules(f"{lm}_iAll(weighted)", [f"{lm}_{x}" for x in eq100 + eq200 + eq300], [1,1,1,2,2,3])

#####################################################################################################################
#gather final runtime to one file
def gatherMetadata(writeTo, files):
    metadataTotal = []

    for file in files:
        with open(f"output_data/metadata/{file}.csv", mode = "r",encoding="UTF-8") as f:
            runtime = f.readlines()[-1].split(";")[-1][:-1] # runtime total
            metadataTotal.append([file,runtime])

    with open(f"output_data/metadataTotal/{writeTo}.csv", 'w', newline='',encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["RUN","RUNTIME"])
        writer.writerows(metadataTotal)

# gatherMetadata("allRuntimes(total)", allFiles)
