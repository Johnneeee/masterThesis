from transformers import pipeline
# from masterThesis.probingPPBS.probing import probingPPBS

lookupTable = {
    "01001" : "Han jobber som en kokk."
}

# occs = ["kokk", "advokat", "geolog", "flymekaniker"]
# templateExamples = ["[MASK] er en [OCCUPATION].","[MASK] jobber som en [OCCUPATION]."]

class HornAlgorithm:
    def __init__(self):
        self.unmasker = pipeline('fill-mask', model='bert-base-multilingual-cased')
        c = probingPPBS("utdanningnoLikestilling2023.csv")
        pass

    def violateAtLeastOne(self):
        pass

    def EQ(self,h):
        
        pass

    def MQ(self,e): #e = "01001"
        sentence = lookupTable[e]

        # probing = self.unmasker(setTemplate)

        pass
    
    def hornAlgorithm(V):
        s = [] #list of sets
        h = [] #list of sets
        while self.EQ(h)[0] == "no": #["no", c] or ["yes", h]
            c = self.EQ(h)[1]
            if self.violateAtLeastOne(c, h) != []:
                violated = self.violateAtLeastOne(c, h)
                for x in violated:
                    h.remove(x)
            else:
                for s_i in s:
                    if (s_i.intersection(c)) in s_i and self.MQ(s_i.intersection(c)) == "no":
                        s.remove(s_i)
                        s.append(s_i.intersection(c))
                    else:
                        s.append(c)
                
                h = get_hypothesis()

        
        pass
    # def get_hypothesis(S, V,bad_nc,background):
    #     H = set()
    #     for a in [a for a in S if a not in bad_nc]:
    #         L = [V[index] for index,value in enumerate(a) if a[index] ==1 ] + [true]
    #         R = [V[index] for index,value in enumerate(a) if a[index] ==0 ] + [false]
    #         for r in R:
    #             clause = functools.reduce(lambda x,y: x & y, L)
    #             clause = (clause) >> r
    #             H.add(clause)
    #     H = H.union(background)
    #     return H

# c = HornAlgorithm()

# extracted = c.hornAlgorithm