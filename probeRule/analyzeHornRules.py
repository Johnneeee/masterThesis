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
eq200 = ["i200_r0","i200_r1","i200_r2"]
eq300 = ["i300_r0","i300_r1","i300_r2"]



# for lm in lms:
#     countRules(f"{lm}_i100", [f"{lm}_{x}" for x in eq100], [1,1,1])
#     countRules(f"{lm}_i200", [f"{lm}_{x}" for x in eq200], [1,1,1])
#     countRules(f"{lm}_i300", [f"{lm}_{x}" for x in eq300], [1,1,1])
# #     countRules(f"{lm}_iAll(weighted)", [f"{lm}_{x}" for x in eq100 + eq200 + eq300], [1,1,1,2,2,3])
#     countRules(f"{lm}_iAll", [f"{lm}_{x}" for x in eq100 + eq200 + eq300], [1,1,1,1,1,1,1,1,1])


# countRules("final_iTotal", allFiles, [1 for _ in range(len(allFiles))])


#####################################################################################################################
# symetric diff
import numpy as np
import matplotlib.pyplot as plt


lms = ["xlmRBase", "xlmRLarge", "mBertUncased", "mBertCased", "nbBertBase", "nbBertLarge", "norbert", "norbert2"]
tags = ["i100_r0","i100_r1","i100_r2","i200_r0","i200_r1","i300_r0"]
allFiles = []

for lm in lms:
    for tag in tags:
        allFiles.append(f"{lm}_{tag}")


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
    return (symdiff, (len(symdiff)))

def createSymdiffMatrix(itag):
    matrix = []
    for f1 in lms:
        vector = []
        for f2 in lms:
            vector.append(symdiff(f"{f1 + itag}",f"{f2 + itag}")[1])
        matrix.append(vector)
    return matrix

iAll = createSymdiffMatrix("_iAll")
lms_ = ["xlmRB", "xlmRL", "mBU", "mBC", "nbBB", "nbBL", "norb", "norb2"]



# plt.imshow(iAll, cmap='RdYlGn_r', interpolation='nearest')
# plt.xticks(ticks=np.arange(len(lms_)), labels=lms_, rotation=30)
# plt.yticks(ticks=np.arange(len(lms_)), labels=lms_)
# plt.title("Heatmap")
# plt.colorbar()
# plt.show()



fig, ax = plt.subplots()
im = ax.imshow(iAll, cmap='RdYlGn_r', interpolation='nearest')

# Tick labels
ax.set_xticks(np.arange(len(lms_)))
ax.set_yticks(np.arange(len(lms_)))
ax.set_xticklabels(lms_, rotation=30)
ax.set_yticklabels(lms_)

# Loop over data dimensions and create text annotations.
ax.text(-2.3, -0.77, "Total disagreement", ha="center", va="center")

for x in range(len(iAll)):
    ax.text(-2.3, x, f"{sum(iAll[x])} - ", ha="center", va="center")
    for y in range(len(iAll)):
        ax.text(x, y, f"{int(iAll[x][y])}", ha="center", va="center")

# for x in range 

# ax.set_title("Heatmap")
# fig.colorbar(im)
# plt.tight_layout()
# plt.show()


genders = ["kvinne", "mann"]
ages = ["yngre enn 20", "mellom 20 og 30", "mellom 30 og 40", "mellom 40 og 50", "mellom 50 og 60", "eldre enn 60"]
occupations = ["advokat","elektriker","rørlegger","modell","sykepleier","frisør","fotograf","forfatter"]
cities = ["Oslo", "Kristiansand", "Stavanger", "Bergen", "Ålesund", "Trondheim", "Bodø", "Tromsø"]
ethnicities = ["Asia", "Afrika", "Nord Amerika", "Sør Amerika", "Europa", "Australia"]



def lol(token):
    if token in genders:    return 0
    if token in ages:       return 1
    if token in occupations:return 2
    if token in cities:     return 3
    if token in ethnicities:return 4
    
with open(f"output_data/runsFilteredTotal/final_iTotal.csv", mode = "r",encoding="UTF-8") as f:
    data = f.readlines()[1:]
    data = list(map(lambda x: x.split(";"),data))
    data = list(map(lambda x: [x[0], x[1].split(" ---> ")[0].split(" & "), x[1].split(" ---> ")[1]],data))
    data = list(map(lambda x: [x[0], sorted(x[1], key = lol),x[2]],data))
    data = list(map(lambda x: f"{x[0]} ; {' & '.join(x[1])} ---> {x[2]}", data))
    # print(data[:10])

    data = list(map(lambda x: x.replace("&", "\&"), data))
    data = list(map(lambda x: x.replace(";", "&"), data))

    rank = 0
    top = 10000
    j = 0
    for i in range(100):
        n = int(data[i][:-1].split("/")[0])
        if n < top:
            top = n
            rank += 1
        text = f" {i+1} & {rank} & {data[i][:-1]} \\\\ \hline" 
        # if ("kvinne" in text) and ("---> FALSE" in text) and any(n in text for n in occupations) and (text.count("&") == 4):
        # if ("mann" in text) and ("---> FALSE" in text) and any(n in text for n in occupations) and (text.count("&") == 4):
        # if ("kvinne" in text) and ("---> FALSE" in text) and any(n in text for n in occupations) and (text.count("&") == 5):
        # if ("mann" in text) and ("---> FALSE" in text) and any(n in text for n in occupations) and (text.count("&") == 5):
    
        # if ("---> kvinne" in text):
        # if ("---> mann" in text):

        if ("kvinne" in text) and (" ---> kvinne" not in text) and not any(n in text for n in occupations):
        # if ("kvinne" in text) and ("---> FALSE" not in text) and ("---> kvinne" not in text):
        # if ("mann" in text) and ("---> FALSE" not in text) and ("---> mann" not in text):
            print(text)
