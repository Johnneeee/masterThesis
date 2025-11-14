import csv

#getting available filenames
lms = ["xlmRBase", "xlmRLarge", "mBertUncased", "mBertCased", "nbBertBase", "nbBertLarge", "norbert", "norbert2"]
tags = ["i100_r0","i100_r1","i100_r2","i200_r0","i200_r1","i200_r2","i300_r0","i300_r1","i300_r2"]
allFiles = []

for lm in lms:
    for tag in tags:
        allFiles.append(f"{lm}_{tag}")

#####################################################################################################################
# Filter Runs
def filterHornRules(filterFile):
    with open(f"input_data/backgroundRules.csv", mode = "r",encoding="UTF-8") as file:
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

# for file in allFiles:
#     filterHornRules(file)

#####################################################################################################################
# # Concat runs
def countRules(writeTo, files):
    countRules = {}
    for i in range(len(files)):
        with open(f"output_data/runsFiltered/{files[i]}.csv", mode = "r",encoding="UTF-8") as f:
            csvFile = csv.reader(f, delimiter=";")
            next(csvFile)
            for line in csvFile:
                rule = line[0]
                try:
                    countRules[rule] += 1
                except:
                    countRules[rule] = 1
    
    rules = [[f"{x[1]}/{len(files)}",x[0]] for x in countRules.items()]
    rules.sort(key=lambda x: int(x[0].split("/")[0]),reverse=True)

    with open(f"output_data/runsFilteredTotal/{writeTo}.csv", 'w', newline='',encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["COUNT","HORN RULES (filtered)"])
        writer.writerows(rules)

# for lm in lms:
#     countRules(f"{lm}_i100", [f"{lm}_{x}" for x in tags[:3]])
#     countRules(f"{lm}_i200", [f"{lm}_{x}" for x in tags[3:6]])
#     countRules(f"{lm}_i300", [f"{lm}_{x}" for x in tags[6:]])
#     countRules(f"{lm}_iAll", [f"{lm}_{x}" for x in tags])


#####################################################################################################################

def combineTopTen(writeTo, files):
    countRules = {}
    for i in range(len(files)):
        with open(f"output_data/runsFilteredTotal/{files[i]}.csv", mode = "r",encoding="UTF-8") as f:
            csvFile = csv.reader(f, delimiter=";")
            next(csvFile)
            linecount = 0
            for line in csvFile:
                if linecount >= 10:
                    break
                count = int(line[0].split("/")[0])
                rule = line[1]
                try:
                    countRules[rule] += count
                except:
                    countRules[rule] = count
                linecount += 1
    
    rules = [[f"{x[1]}/72",x[0]] for x in countRules.items()]
    rules.sort(key=lambda x: int(x[0].split("/")[0]),reverse=True)

    with open(f"output_data/runsFilteredTotal/{writeTo}.csv", 'w', newline='',encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["COUNT","HORN RULES (filtered)"])
        writer.writerows(rules)

# combineTopTen("combineFromTopTen", [f"{lm}_iAll" for lm in lms])

#####################################################################################################################
