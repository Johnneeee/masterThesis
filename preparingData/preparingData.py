import csv
def prepareDistnctNames(read,write):
    names = []
    with open(read, mode ='r', encoding="UTF-8") as file:
        csvFile = csv.reader(file, delimiter=";")
        next(csvFile)
        for lines in csvFile:
                names += lines[1:] #excluding year

    names = list(set(names)) #distinct names
    names = list(map(lambda x: x[0] + x[1:].lower(),names)) # lower [1:] eg: MARKUS -> Markus
    names = [[x] for x in names]

    head = [["DISTNCT NAMES"]]
    with open(write, 'w', newline='', encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerows(head)
        writer.writerows(names)

def prepareAddPPBS(read,write):
    data = []
    with open(read, encoding = "UTF-8") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader) # skip first line which includes the description, ie [occupation, female, male]
        for line in reader:
            occ = line[0].lower()
            she = round(float(line[1])/100, 3) # /100 to turn into percentage
            he = round(float(line[2])/100, 3)
            gold_ppbs = round(he-she,3)
            data.append([occ,she,he,gold_ppbs])

    head = [["OCCUPATION", "p(SHE)", "p(HE)", "ppbs"]]
    with open(write, 'w', newline='', encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerows(head)
        writer.writerows(data)
    # return data # [[occ,p_she,p_he,gold_ppbs]]
    pass

prepareDistnctNames("../censusData/ssbTopJentenavn80-23.csv", "../censusData/preparedData/ssbTopJentenavn80-23_distinct.csv")
prepareDistnctNames("../censusData/ssbTopGuttenavn80-23.csv", "../censusData/preparedData/ssbTopGuttenavn80-23_distinct.csv")

prepareAddPPBS("../censusData/utdanningnoLikestilling2023.csv", "../censusData/preparedData/utdanningnoLikestilling2023_ppbs.csv")
