# dictionary = {}
# with open(f"../censusData/preparedData/utdanningnoLikestilling2023_prepared.csv", mode = "r",encoding="UTF-8") as f:
#     # OCCUPATION;p(SHE);p(HE);ppbs(gold)
#     data = f.readlines()[1:]
#     data = [x.split(";")[0] for x in data]
#     data.sort()

#     for i in range(len(data)):
#         dictionary[data[i]] = i

# # print(dictionary)


# # print(list(dictionary.keys()))
# # totalData = [[str(i)] for i in range(1,451)]
# totalData = [[x] for x in list(dictionary.keys())]


# lms = [
#     "data/raw/xlmRBase_ppbs.csv",
#     "data/raw/xlmRLarge_ppbs.csv",
#     "data/raw/mBertUncased_ppbs.csv",
#     "data/raw/mBertCased_ppbs.csv",
#     "data/raw/nbBertBase_ppbs.csv",
#     "data/raw/nbBertLarge_ppbs.csv",
#     "data/raw/norbert_ppbs.csv",
#     "data/raw/norbert2_ppbs.csv",    
#     "data/total/total_ppbs.csv",    
# ]

# for lm in lms:
#     with open(lm, mode = "r",encoding="UTF-8") as f:
#         # attribute, gold, pred
#         data = f.readlines()[1:]
#         data = [x.split(";") for x in data]
#         data = [[x[0],x[2][:-1]] for x in data]
#         for x in data:
#             totalData[dictionary[x[0]]-1].append(x[1])



# with open(lm, mode = "r",encoding="UTF-8") as f:
#     # attribute, gold, pred
#     data = f.readlines()[1:]
#     data = [x.split(";") for x in data]
#     data = [[x[0],x[1]] for x in data]
#     for x in data:
#         totalData[dictionary[x[0]]-1].append(x[1])


# for x in totalData:
#     print(f'{" & ".join(x)} \\\\ \hline')
####################################################################

dictionary = {}

with open(f"../probePPBS/data/total/total_ppbs.csv", mode = "r",encoding="UTF-8") as f:
    data = f.readlines()[1:]
    # print(data[1])
    data = [x.split(";") for x in data]
    for x in data:
        dictionary[x[0]] = x[2][:-1]

# print(dictionary)
totalData = []
with open(f"data/total/totalFiltered_occ.csv", mode = "r",encoding="UTF-8") as f:
# with open(f"data/filtered/norbert2Filtered_occ.csv", mode = "r",encoding="UTF-8") as f:
# with open(f"data/total/totalFiltered_occ.csv", mode = "r",encoding="UTF-8") as f:
    data = f.readlines()[1:]
    data = [x.split(";") for x in data]
    totalData = [[x[0],str(int(x[1])+int(x[2]))] for x in data]
    # totalData = [[x[0],x[1],x[2],str(int(x[1])+int(x[2])),x[3],x[4],x[5],x[6][:-1]] for x in data]
    totalData.sort(key=lambda x: int(x[1]),reverse=True)
    # totalData.sort(key=lambda x: float(x[-2]))
    # print(totalData)
    # totalData = [[x[0],str(int(x[1])+int(x[2])),dictionary[x[0]],x[5],str(round(((float(x[5])+float(dictionary[x[0]]))/2),3)),x[6][:-1]] for x in data]
    # totalData.sort(key=lambda x: float(x[-2]))

    # totalData = [[x[0],int(x[1])+int(x[2]),x[5]] for x in data]

# print(totalData)
st = totalData[:20]
nd = totalData[20:40]
rd = totalData[40:] + ["",""]

total = []
print(len(st))
print(len(nd))
print(len(rd))

for i in range(20):
    print(f"{' & '.join(st[i])} & {' & '.join(nd[i])} & {' & '.join(rd[i])} \\\\ \hline")

# fsm bfl fah bjm asl krj gfg apr lps fam tff smm rpk ipr opv pek jra esd bldl
# fsm bff