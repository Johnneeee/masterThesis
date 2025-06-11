import csv
import datetime

#getting available filenames
lms = ["xlmRBase", "xlmRLarge", "mBertUncased", "mBertCased", "nbBertBase", "nbBertLarge", "norbert", "norbert2"]
tags = ["i100_r0","i100_r1","i100_r2","i200_r0","i200_r1","i300_r0"]
allFiles = []

for lm in lms:
    for tag in tags:
        allFiles.append(f"{lm}_{tag}")


#####################################################################################################################
def addTotalRuntime(file):
    newData = []
    with open(f"output_data/metadataRaw/{file}.csv", mode = "r",encoding="UTF-8") as f:
        totalRt = 0
        csvFile = csv.reader(f, delimiter=";")
        next(csvFile)
        for line in csvFile:
            totalRt = round(totalRt + float(line[-1]),3)
            newline = line + [totalRt] + [str(datetime.timedelta(seconds=int(totalRt)))]
            newData.append(newline)

    with open(f"output_data/metadataTotalRuntime/{file}.csv", 'w', newline='',encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["ITERATION","LEN(HYP)","SAMPLENR","RUNTIME(sample)","RUNTIME(total)s","RUNTIME(total)"])
        writer.writerows(newData)

for file in allFiles:
    addTotalRuntime(file)

# addTotalRuntime("ahahhahahah_i10_r0")
#####################################################################################################################
#gather final runtime to one file
def gatherMetadata(writeTo, files):
    metadataTotal = []

    for file in files:
        with open(f"output_data/metadataRaw/{file}.csv", mode = "r",encoding="UTF-8") as f:
            runtime = f.readlines()[-1].split(";")[-1][:-1] # runtime total
            metadataTotal.append([file,runtime])

    with open(f"output_data/metadataAll/{writeTo}.csv", 'w', newline='',encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["RUN","RUNTIME"])
        writer.writerows(metadataTotal)

gatherMetadata("allRuntimes(all)", allFiles)
