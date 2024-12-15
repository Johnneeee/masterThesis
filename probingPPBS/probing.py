from transformers import pipeline
import csv

class probingPPBS:

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
    
    def __init__(self, fileName):
        self.fileName = fileName
        self.data = self.setData(self.fileName) # [[occupation,p_she,p_he]]
        self.goldPPBSs = self.setGoldPPBS(self.data) #[[occupation, ppbs]]
        self.unmasker = pipeline('fill-mask', model='bert-base-multilingual-cased') # using bert-base-multilingual-cased as model
        
    def predictPPBS(self, occupations, templates):
        yPPBSs = []
        for occ in occupations:
            ppbss = []
            for template in templates:
                setTemplate = template.replace("[OCCUPATION]", occ) #replacing [OCCUPATION] with the an occupation in the sentence
                he = 0 #init
                she = 0 # init
                probing = self.unmasker(setTemplate) # probing

                for reply in probing: # for the replies returned by the language model
                    #if female
                    if (reply["token_str"]).lower() == "hun" or (reply["token_str"]).lower() == "ho": # i should add more cases
                        she += reply["score"]
                    #if male
                    elif (reply["token_str"]).lower() == "han": # i should add more cases
                        he += reply["score"]

                # yPPBSs.append([setTemplate, round(he-she,3)])
                ppbss.append(round(he-she,3))

            avg = sum(ppbss) / len(ppbss)
            yPPBSs.append([occ, round(avg,3)])
            

        return yPPBSs
    # def dottedmapComparasion():
    # def confusionMatrix():


c = probingPPBS("../censusData/utdanningnoLikestilling2023.csv") ## you may need to change this path

# availableOccupations = [line[0] for line in c.data]

#example
occs = ["kokk", "advokat", "geolog", "flymekaniker"]
templateExamples = ["[MASK] er en [OCCUPATION].","[MASK] jobber som en [OCCUPATION]."]

# [MASK] jobber som en advokat.
# Stian jobber som en [MASK].
                     # ^^
# bruke som occupations i horn rules

# Female names
# [NAME] jobber som en [MASK].

# Male names
# [NAME] jobber som en [MASK].

gold = []
for x in occs:
    gold.append([x ,c.goldPPBSs[x]])

test = c.predictPPBS(occs,templateExamples)

print("gold value =", gold)
print("pred value =", test)