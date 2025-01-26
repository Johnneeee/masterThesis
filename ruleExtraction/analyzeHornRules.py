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

    with open(f"output_data/runsFiltered/{filterFile}19191919.csv", 'w', newline='',encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["HORN RULES (filtered)"])
        writer.writerows(hornRules)

# tags = ["i100_r0","i100_r1","i100_r2","i200_r0","i200_r1","i300_r0"]
# for x in tags: filterHornRules(f"xlmRBase_{x}")
# for x in tags: filterHornRules(f"xlmRLarge_{x}")
# for x in tags: filterHornRules(f"mBertUncased_{x}")
# for x in tags: filterHornRules(f"mBertCased_{x}")
# for x in tags: filterHornRules(f"nbBertBase_{x}")
# for x in tags: filterHornRules(f"nbBertLarge_{x}")
# for x in tags: filterHornRules(f"norbert_{x}")
# for x in tags: filterHornRules(f"norbert2_{x}")

# # Concat runs
# #################
def countRules(writeTo, files):
    n = len(files)
    countRules = {}
    for file in files:
        with open(f"output_data/runsFiltered/{file}.csv", mode = "r",encoding="UTF-8") as f:
            csvFile = csv.reader(f, delimiter=";")
            next(csvFile)
            for line in csvFile:
                rule = line[0]
                try:
                    countRules[rule] += 1
                except:
                    countRules[rule] = 1
    
    rules = [[f"{x[1]}/{n}",x[0]] for x in countRules.items()]
    rules.sort(key=lambda x: int(x[0].split("/")[0]),reverse=True)

    with open(f"output_data/runsFilteredTotal/{writeTo}.csv", 'w', newline='',encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["COUNT","EXTRACTED HORN RULES"])
        writer.writerows(rules)

eq100 = ["i100_r0","i100_r1","i100_r2"]
eq200 = ["i200_r0","i200_r1"]
eq300 = ["i300_r0"]
# countRules("xlmRBase_i100", [f"xlmRBase_{x}" for x in eq100])
# countRules("xlmRBase_i200", [f"xlmRBase_{x}" for x in eq200])
# countRules("xlmRBase_i300", [f"xlmRBase_{x}" for x in eq300])
# countRules("xlmRBase_iAll", [f"xlmRBase_{x}" for x in eq100 + eq200 + eq300])

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

gatherMetadata("xlmBase", [f"xlmRBase_{x}" for x in eq100 + eq200 + eq300])