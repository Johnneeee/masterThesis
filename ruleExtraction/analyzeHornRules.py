import csv
import matplotlib.pyplot as plt
import numpy as np

#getting available filenames
lms = ["xlmRBase", "xlmRLarge", "mBertUncased", "mBertCased", "nbBertBase", "nbBertLarge", "norbert", "norbert2"]
tags = ["i100_r0","i100_r1","i100_r2","i200_r0","i200_r1","i300_r0"]
allFiles = []

for lm in lms:
    for tag in tags:
        allFiles.append(f"{lm}_{tag}")

#####################################################################################################################
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

# for file in allFiles:
#     filterHornRules(file)

#####################################################################################################################
# adding guiding comments
def addGuide(dataFile):
    with open(f"input_data/ethnicityValues.csv", mode = "r",encoding="UTF-8") as file:
        csvFile = csv.reader(file, delimiter=";")
        next(csvFile)
        ethnicity = [x[0] for x in csvFile]
        print(ethnicity)

    with open(f"input_data/cityValues.csv", mode = "r",encoding="UTF-8") as file:
        csvFile = csv.reader(file, delimiter=";")
        next(csvFile)
        city = [x[0] for x in csvFile]
        print(city)

    with open(f"output_data/runsFiltered/{dataFile}.csv", mode = "r",encoding="UTF-8") as file:
        csvFile = csv.reader(file, delimiter=";")
        next(csvFile)
        hornRules = [x for x in csvFile]
        print(hornRules)

    for i in range(len(hornRules)):
        for x in city:
            hornRules[i] = [hornRules[i][0].replace(x,f"{x}(residence)")]
        for x in ethnicity:
            hornRules[i] = [hornRules[i][0].replace(x,f"{x}(ethnicity)")]

    with open(f"output_data/runsFiltered/fake{dataFile}.csv", 'w', newline='',encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["HORN RULES (filtered + guide tags)"])
        writer.writerows(hornRules)

# for file in allFiles:
#     addGuide(file)

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
#     countRules(f"{lm}_i100", [f"{lm}_{x}" for x in eq100], [1,1,1])
#     countRules(f"{lm}_i200", [f"{lm}_{x}" for x in eq200], [1,1])
#     countRules(f"{lm}_i300", [f"{lm}_{x}" for x in eq300], [1])
#     countRules(f"{lm}_iAll(weighted)", [f"{lm}_{x}" for x in eq100 + eq200 + eq300], [1,1,1,2,2,3])
#####################################################################################################################
# symetric diff heatmap

def formatData(file):
    with open(f"output_data/runsFilteredTotal/{file}.csv", mode = "r",encoding="UTF-8") as f:
        data = f.readlines()[1:]
        data = list(map(lambda x: x.split(";")[1].split(" ---> "),data)) # seperate ant and con
        data = list(map(lambda x: (set(x[0].split(" & ")), x[1]),data)) # seperate ant on &

    return data

def symdiff(file1, file2):
    data1 = formatData(file1)
    data2 = formatData(file2)
    concat = data1 + data2

    mutual = list(filter(lambda x: x in data1, data2))
    symdiff = list(filter(lambda x: x not in mutual, concat))
    return (symdiff, len(symdiff))

def createSymdiffMatrix(itag):
    matrix = []
    for f1 in lms:
        vector = []
        for f2 in lms:
            vector.append(symdiff(f"{f1 + itag}",f"{f2 + itag}")[1])
        matrix.append(vector)
    return matrix

# i100 = createSymdiffMatrix("_i100")
# i200 = createSymdiffMatrix("_i200")
# i300 = createSymdiffMatrix("_i300")
# iAll = createSymdiffMatrix("_iAll(weighted)")

# lms_ = ["xlmRB", "xlmRL", "mBU", "mBC", "nbBB", "nbBL", "norb", "norb2"]
# figure, axis = plt.subplots(2, 2, figsize=(12, 12))

# def setHeatmap(matrix, title, position):
#     x,y = position
#     axis[x, y].imshow(matrix, cmap='RdYlGn_r', interpolation='nearest')
#     axis[x, y].set_xticks(ticks=np.arange(len(lms_)), labels=lms_, rotation=30)
#     axis[x, y].set_yticks(ticks=np.arange(len(lms_)), labels=lms_)
#     axis[x, y].set_title(title)

# setHeatmap(i100, "i100", [0,0])
# setHeatmap(i200, "i200", [0,1])
# setHeatmap(i300, "i300", [1,0])
# setHeatmap(iAll, "iAll", [1,1])
# plt.show()