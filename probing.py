from transformers import pipeline

class probingPPBS:
    def __init__(self, fileName):
        self.fileName = fileName
        # self.templateSentences = templateSentences
        self.data = []
        self.goldPPBSs = []
        self.unmasker = pipeline('fill-mask', model='bert-base-multilingual-cased') # using bert-base-multilingual-cased as model


    def setData(self, fileName): # setting data
       with open(fileName, encoding = "UTF-8") as f:
            next(f) # skip first line which includes the description, ie [occupation, female, male]
            for line in f:
                # formatting
                listLine = line[:-1].split(";")
                occ = listLine[0].lower()
                she = round(float(listLine[1])/100, 3) # /100 to turn into percentage
                he = round(float(listLine[2])/100, 3)

                self.data.append([occ,she,he])
                # break

    def setGoldPPBS(self, data): # setting goldPPBS
        for x in data:
            self.goldPPBSs.append([x[0], round(x[1]-x[2], 3)]) #[occupation, ppbs]
            # break

    def init(self):
        self.setData(self.fileName)
        self.setGoldPPBS(self.data)
        
    def predictPPBS(self, templates):
        yPPBSs = []
        occupations = list(map(lambda x: x[0], self.data)) #list if all occupations from data        
        for template in templates:

            for occ in occupations[:3]: #limiting to 3 during testing
                setTemplate = template.replace("[ATTRIBUTE]", occ) #replacing [ATTRIBUTE] with the an occupation in the sentence
                he = 0 #init
                she = 0 # init
                probing = self.unmasker(setTemplate) # probing

                for reply in probing: # for the replies returned by the language model
                    #if female
                    if reply["token_str"] == "Hun" or reply["token_str"] == "hun": # i should add more cases
                        she += reply["score"]
                    #if male
                    elif reply["token_str"] == "Han" or reply["token_str"] == "han": # i should add more cases
                        he += reply["score"]

                yPPBSs.append([setTemplate, round(he-she,3)])

        return yPPBSs


c = probingPPBS("utdanningnoLikestilling2023.csv") ## you may need to change this path
c.init()

templateExamples = ["[MASK] er en [ATTRIBUTE].","[MASK] jobber som en [ATTRIBUTE]."]

test = c.predictPPBS(templateExamples)
print(test)