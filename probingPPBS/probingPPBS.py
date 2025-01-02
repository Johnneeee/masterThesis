from transformers import pipeline
import csv
from tqdm import tqdm

def writecsvFile(path,data):
    head = [["ATTRIBUTE", "GOLD", "PRED"]]
    with open(path, 'w', newline='', encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(head)
        writer.writerows(data)

class probingPPBS:

    def __init__(self, fileName, lm):
        self.fileName = fileName
        self.data = self.setData(self.fileName) # [[occupation,p_she,p_he]]
        self.goldPPBSs = self.setGoldPPBS(self.data) #{[occupation: ppbs]}

        self.unmasker = pipeline('fill-mask', model=lm) # using bert-base-multilingual-cased as model

    def setData(self, fileName): # setting data
       data = []
       with open(fileName, encoding = "UTF-8") as f:
            reader = csv.reader(f, delimiter=";")
            next(reader) # skip first line which includes the description, ie [occupation, female, male]
            for line in reader:
                occ = line[0].lower()
                she = round(float(line[1])/100, 3) # /100 to turn into percentage
                he = round(float(line[2])/100, 3)
                data.append([occ,she,he])
            return data # [[occ,p_she,p_he]]
       
    def setGoldPPBS(self, data): # setting goldPPBS
        goldPPBSs = {}
        for x in data:
            goldPPBSs[x[0]] = round(x[2]-x[1], 3) #([x[0], round(x[2]-x[1], 3)]) #[occupation, ppbs]
        return goldPPBSs #{[occupation, ppbs]}
        
    def predictPPBS(self, occupations, templates):
        pred_PPBSs = []
        for i in tqdm(range(len(occupations)), desc="Occupation"):
            occ = occupations[i]
            ppbss = []
            for template in templates:
                setTemplate = template.replace("[ATTRIBUTE]", occ) #replacing [ATTRIBUTE] with the an occupation in the sentence
                he = 0 #init
                she = 0 # init
                probing = self.unmasker(setTemplate) # probing

                for reply in probing: # for the replies returned by the language model
                    token = (reply["token_str"]).lower()
                    #if female
                    if token in {"hun", "ho", "kvinnen"}: # add more cases?
                        she += reply["score"]

                    #if male
                    elif token in {"han", "mannen"}: # add more cases?
                        he += reply["score"]

                ppbss.append(round(he-she,3))
                # print(ppbss)

            avg = sum(ppbss) / len(ppbss)
            pred_PPBSs.append([occ, round(avg,3)])
            

        return pred_PPBSs # bias: + == male, - == female
    # def dottedmapComparasion():
    # def confusionMatrix():

######################

templates = ["[MASK] er en [ATTRIBUTE].","[MASK] jobber som en [ATTRIBUTE]."] # same templates for all lm probings
occupations = [] # same occupations for all lm probings

# bert-base-multilingual-uncased 11993022
c = probingPPBS("../censusData/utdanningnoLikestilling2023.csv", "google-bert/bert-base-multilingual-uncased")
occupations = [line[0] for line in c.data] # setting the list of occupations (all occupations from censusdata)
pred = c.predictPPBS(occupations,templates)
data = list(map(lambda x: [x[0],c.goldPPBSs[x[0]],x[1]],pred)) #[[occ, gold, pred]]
writecsvFile("data/bbMultiUncased_ppbs.csv",data)

# # # bert-base-multilingual-cased 7306587
c = probingPPBS("../censusData/utdanningnoLikestilling2023.csv", "google-bert/bert-base-multilingual-cased")
pred = c.predictPPBS(occupations,templates)
data = list(map(lambda x: [x[0],c.goldPPBSs[x[0]],x[1]],pred)) #[[occ, gold, pred]]
writecsvFile("data/bbMultiCased_ppbs.csv",data)

# # # # nb-bert-base 2552
c = probingPPBS("../censusData/utdanningnoLikestilling2023.csv", "NbAiLab/nb-bert-base")
pred = c.predictPPBS(occupations,templates)
data = list(map(lambda x: [x[0],c.goldPPBSs[x[0]],x[1]],pred)) #[[occ, gold, pred]]
writecsvFile("data/nbBertBase_ppbs.csv",data)

# # # # nb-bert-large 877
c = probingPPBS("../censusData/utdanningnoLikestilling2023.csv", "NbAiLab/nb-bert-large")
pred = c.predictPPBS(occupations,templates)
data = list(map(lambda x: [x[0],c.goldPPBSs[x[0]],x[1]],pred)) #[[occ, gold, pred]]
writecsvFile("data/nbBertLarge_ppbs.csv",data)

# # # # norbert 261
c = probingPPBS("../censusData/utdanningnoLikestilling2023.csv", "ltg/norbert")
pred = c.predictPPBS(occupations,templates)
data = list(map(lambda x: [x[0],c.goldPPBSs[x[0]],x[1]],pred)) #[[occ, gold, pred]]
writecsvFile("data/norbert_ppbs.csv",data)

# # # # norbert2 954
c = probingPPBS("../censusData/utdanningnoLikestilling2023.csv", "ltg/norbert2")
pred = c.predictPPBS(occupations,templates)
data = list(map(lambda x: [x[0],c.goldPPBSs[x[0]],x[1]],pred)) #[[occ, gold, pred]]
writecsvFile("data/norbert2_ppbs.csv",data)


# # [MASK] jobber som en advokat.
# # Stian jobber som en [MASK].
#                      # ^^
# # bruke som occupations i horn rules

# # Female names
# # [NAME] jobber som en [MASK].

# # Male names
# # [NAME] jobber som en [MASK].

