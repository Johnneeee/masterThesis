from transformers import pipeline
import csv

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
        return goldPPBSs #[[occupation, ppbs]]
        
    def predictPPBS(self, occupations, templates):
        yPPBSs = []
        for occ in occupations:
            ppbss = []
            for template in templates:
                setTemplate = template.replace("[ATTRIBUTE]", occ) #replacing [OCCUPATION] with the an occupation in the sentence
                he = 0 #init
                she = 0 # init
                probing = self.unmasker(setTemplate) # probing

                for reply in probing: # for the replies returned by the language model
                    #if female
                    if (reply["token_str"]).lower() == "hun" or (reply["token_str"]).lower() == "ho": # i should add more cases
                        she += reply["score"]
                        print(f"henne {reply['score']}")
                    #if male
                    elif (reply["token_str"]).lower() == "han": # i should add more cases
                        he += reply["score"]
                        print(f"han {reply['score']}")


                # yPPBSs.append([setTemplate, round(he-she,3)])
                ppbss.append(round(he-she,3))
                print(ppbss)

            avg = sum(ppbss) / len(ppbss)
            yPPBSs.append([occ, round(avg,3)])
            

        return yPPBSs
    # def dottedmapComparasion():
    # def confusionMatrix():


c = probingPPBS("../censusData/utdanningnoLikestilling2023.csv", "bert-base-multilingual-cased") ## you may need to change this path

# availableOccupations = [line[0] for line in c.data]

#example
# occs = ["kokk", "advokat", "geolog", "flymekaniker", "dyrepleier"]
occs = ["dyrepleier"] #0.63
templateExamples = ["[MASK] er en [ATTRIBUTE].","[MASK] jobber som en [ATTRIBUTE]."]

# [MASK] jobber som en advokat.
# Stian jobber som en [MASK].
                     # ^^
# bruke som occupations i horn rules

# Female names
# [NAME] jobber som en [MASK].

# Male names
# [NAME] jobber som en [MASK].

# gold = []
# for x in occs:
#     gold.append([x ,c.goldPPBSs[x]])

# [['kokk', 0.205], ['advokat', 0.383], ['geolog', 0.138], ['flymekaniker', 0.242]]
pred = c.predictPPBS(occs,templateExamples)

# adding gold next to each for pred for comparason
# [['kokk', 0.184, 0.205], ['advokat', 0.02, 0.383], ['geolog', 0.338, 0.138], ['flymekaniker', 0.886, 0.242]]
data = list(map(lambda x: [x[0],c.goldPPBSs[x[0]],x[1]],pred)) #[[occ, gold, pred]]
print(data)
# head = [["ATTRIBUTE", "GOLD", "PRED"]]
# with open('probingPPBS_Data.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerows(head)
#     writer.writerows(data)