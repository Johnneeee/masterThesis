import csv
# ##########################################################################

def filterOcc(file): # filtered
    # getting gold data
    with open(f"../censusData/preparedData/utdanningnoLikestilling2023_prepared.csv", mode ='r', encoding="UTF-8") as f:
        csvFile = csv.reader(f, delimiter=";")
        next(csvFile)
        gold_data = {x[0]: float(x[3]) for x in csvFile}

    #getting pred data
    with open(f"data/raw/{file}_occ.csv", mode ='r', encoding="UTF-8") as f:
        csvFile = csv.reader(f, delimiter=";")
        next(csvFile)
        data = [x for x in csvFile]

    data = list(filter(lambda x: x[0] in gold_data, data)) # filter data
    data = [x + [gold_data[x[0]]] for x in data] # adding gold ppbs in end of list

    #write data
    head = [["ATTRIBUTE", "COUNT FEMALE", "COUNT MALE", "P(FEMALE)", "P(MALE)", "P(PPBS)", "GOLD PPBS"]]
    with open(f"data/filtered/{file}Filtered_occ.csv", 'w', newline='', encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerows(head)
        writer.writerows(data)

# lms = ["xlmRBase", "xlmRLarge", "mBertUncased", "mBertCased", "nbBertBase", "nbBertLarge", "norbert", "norbert2"]
# for name in lms:
#     filterOcc(name)

# ##########################################################################

def total(files, tag): # total/totalFiltered
    occAppearnceCount = {}
    totalData = {}
    for file in files:
        with open(f"data/{tag}/{file}_occ.csv", mode ='r', encoding="UTF-8") as f:
            csvFile = csv.reader(f, delimiter=";")
            next(csvFile)
            for line in csvFile:
                try: # update
                    occAppearnceCount[line[0]] += 1
                    totalData[line[0]][0] += int(line[1])    #count she
                    totalData[line[0]][1] += int(line[2])    #count he
                    totalData[line[0]][2] = round(totalData[line[0]][2] + float(line[3]),3)  #pshe 
                    totalData[line[0]][3] = round(totalData[line[0]][3] + float(line[4]),3)  #phe
                    totalData[line[0]][4] = round(totalData[line[0]][4] + float(line[5]),3)  #pshe 
                except: # set
                    occAppearnceCount[line[0]] = 1
                    totalData[line[0]] = [int(x) for x in line[1:3]] + [float(x) for x in line[3:]]
    for x in totalData: # average out
        totalData[x][2] = round(totalData[x][2]/occAppearnceCount[x],3) #pshe
        totalData[x][3] = round(totalData[x][3]/occAppearnceCount[x],3) #phe
        totalData[x][4] = round(totalData[x][4]/occAppearnceCount[x],3) #ppbs
    
    # format data before writing
    head = [["ATTRIBUTE", "COUNT FEMALE", "COUNT MALE", "P(FEMALE)", "P(MALE)", "P(PPBS)", "GOLD PPBS"]]
    if tag == "raw":
        head = [["ATTRIBUTE", "COUNT FEMALE", "COUNT MALE", "P(FEMALE)", "P(MALE)", "P(PPBS)"]]
    data = [[x[0]] + x[1] for x in totalData.items()]
    data = sorted(data, key=lambda x: max(x[1], x[2]),reverse=True)

    # writing data
    with open(f"data/total/total{tag[0].upper() + tag[1:]}_occ.csv", 'w', newline='', encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerows(head)
        writer.writerows(data)


lms = ["xlmRBaseFiltered", "xlmRLargeFiltered", "mBertUncasedFiltered", "mBertCasedFiltered", "nbBertBaseFiltered", "nbBertLargeFiltered", "norbertFiltered", "norbert2Filtered"]
total(lms, "filtered")

lms = ["xlmRBase", "xlmRLarge", "mBertUncased", "mBertCased", "nbBertBase", "nbBertLarge", "norbert", "norbert2"]
total(lms, "raw")

# ##########################################################################
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
