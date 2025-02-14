import csv
lms = ["xlmRBase", "xlmRLarge", "mBertUncased", "mBertCased", "nbBertBase", "nbBertLarge", "norbert", "norbert2"]
# ##########################################################################

def filterOcc(file): # filtered
    with open(f"../censusData/preparedData/utdanningnoLikestilling2023_ppbs.csv", mode ='r', encoding="UTF-8") as f:
        csvFile = csv.reader(f, delimiter=";")
        next(csvFile)
        occs = {x[0]: x[3] for x in csvFile}

    with open(f"data/raw/{file}.csv", mode ='r', encoding="UTF-8") as f:
        csvFile = csv.reader(f, delimiter=";")
        next(csvFile)
        data = f.readlines()

    data = [x[:-1].split(";") for x in data] #formatting data
    data = list(filter(lambda x: x[0] in occs, data)) # filter away occs that doesnt appear in census
    data = list(map(lambda x: x + [occs[x[0]]],data))

    head = [["ATTRIBUTE", "COUNT FEMALE", "COUNT MALE", "P(FEMALE)", "P(MALE)", "P(PPBS)", "GOLD PPBS"]]
    with open(f"data/filtered/{file}.csv", 'w', newline='', encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerows(head)
        writer.writerows(data)

# for name in lms:
#     filterOcc(name)

# ##########################################################################

def totalFiltered(files): # total/totalFiltered
    totalData = {}
    for file in files:
        with open(f"data/filtered/{file}.csv", mode ='r', encoding="UTF-8") as f:
            csvFile = csv.reader(f, delimiter=";")
            next(csvFile)
            for line in csvFile:
                try: # update
                    totalData[line[0]][0] += int(line[1])    #count she
                    totalData[line[0]][1] += int(line[2])    #count he
                    totalData[line[0]][2] = round((totalData[line[0]][2] + float(line[3]))/2,3)  #pshe
                    totalData[line[0]][3] = round((totalData[line[0]][3] + float(line[4]))/2,3)  #phe
                    totalData[line[0]][4] = round((totalData[line[0]][4] + float(line[5]))/2,3)  #ppbs
                except: # set
                    totalData[line[0]] = [int(x) for x in line[1:3]] + [float(x) for x in line[3:]]


    head = [["ATTRIBUTE", "COUNT FEMALE", "COUNT MALE", "P(FEMALE)", "P(MALE)", "P(PPBS)", "GOLD PPBS"]]
    data = [[x[0]] + x[1] for x in totalData.items()]
    data = sorted(data, key=lambda x: max(x[1], x[2]),reverse=True)

    with open(f"data/total/totalFiltered.csv", 'w', newline='', encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerows(head)
        writer.writerows(data)

totalFiltered(lms)

# ##########################################################################

def totalRaw(files): # ->total/totalRaw
    totalData = {}
    for file in files:
        with open(f"data/raw/{file}.csv", mode ='r', encoding="UTF-8") as f:
            csvFile = csv.reader(f, delimiter=";")
            next(csvFile)
            for line in csvFile:
                try: # update
                    totalData[line[0]][0] += int(line[1])    #count she
                    totalData[line[0]][1] += int(line[2])    #count he
                    totalData[line[0]][2] = round((totalData[line[0]][2] + float(line[3]))/2,3)  #pshe
                    totalData[line[0]][3] = round((totalData[line[0]][3] + float(line[4]))/2,3)  #phe
                    totalData[line[0]][4] = round((totalData[line[0]][4] + float(line[5]))/2,3)  #ppbs
                except: # set
                    totalData[line[0]] = [int(x) for x in line[1:3]] + [float(x) for x in line[3:]]


    head = [["ATTRIBUTE", "COUNT FEMALE", "COUNT MALE", "P(FEMALE)", "P(MALE)", "P(PPBS)"]]
    data = [[x[0]] + x[1] for x in totalData.items()]
    data = sorted(data, key=lambda x: max(x[1], x[2]),reverse=True)

    with open(f"data/total/totalRaw.csv", 'w', newline='', encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerows(head)
        writer.writerows(data)

totalRaw(lms)
    

# # top 20 female occs:       top 20 male occs:
# # lærer                     lærer,
# # journalist,               skuespiller,
# # modell,                   journalist,
# # skuespiller,              lege,
# # assistent,                fotograf,
# # sykepleier,               advokat,
# # fotograf,                 frisør,
# # frisør,                   elektriker,
# # lærling,                  assistent,
# # advokat,                  lærling,
# # lege,                     snekker,
# # coach,                    trener,
# # frivilling,               musiker,
# # vikar,                    sykepleier,
# # forfatter,                vekter,
# # sekretær,                 sjåfør,
# # hushjelp,                 kokk,
# # kokk,                     politi,
# # bibliotekar,              forfatter,
# # manager                   arkitekt



# # sekretær

# # [Mask] is a manager

# # 1 ppbs
# # 2 occ given name intersect(1,2) (top 5 male/female -> hornrules())
# # 3 horn rules

# # first finding ppbs score for all occupations from the census data                 1
#     # goal: find ppbs score
# # find the occupation given name                                                    2
#     # goal: find which occ the lm "understands as occupations" 
# # find intersection(1,2), choose top x biased occs from male/female (ppbs)          connecting 1,2,3 
#     # goal: find occupation variables for the rules
# # horn rule (maybe other attributes are linked to the occs too)                     3
#     # goal: understand more of gender/occ bias (how it relates to the variables)


# # from top 20:
# # distinct female occs:     distinct male occs:     common occs:
# # modell,                   elektriker,             lærer,
# # coach,                    snekker,                skuespiller,
# # frivilling,               trener,                 journalist,
# # vikar,                    musiker,                lege,
# # sekretær,                 vekter,                 fotograf,
# # hushjelp,                 sjåfør,                 advokat,
# # bibliotekar,              politi,                 frisør,
# # manager,                  arkitekt,               assistent,
# #                                                   lærling,
# #                                                   sykepleier
# #                                                   kokk,
# #                                                   forfatter

# # top 20 
# # male/female for whole data
# # really distinct for all
