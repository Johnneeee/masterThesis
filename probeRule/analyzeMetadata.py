import csv

#getting available filenames
lms = ["xlmRBase", "xlmRLarge", "mBertUncased", "mBertCased", "nbBertBase", "nbBertLarge", "norbert", "norbert2"]
tags = ["i100_r0","i100_r1","i100_r2","i200_r0","i200_r1","i300_r0"]
allFiles = []

for lm in lms:
    for tag in tags:
        allFiles.append(f"{lm}_{tag}")

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
