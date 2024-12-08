from sympy import *
import functools
import random
import timeit
import math
from intepretor import *
from transformers import pipeline


class HornAlgorithm():
    def __init__(self, epsilon, delta, lm, intepretor : Intepretor, V):
        # static
        self.epsilon = epsilon
        self.delta = delta
        self.intepretor = intepretor
        self.hypSpace = math.prod(self.intepretor.lengths.values())*2
        self.sampleSize = int ( (1/epsilon) * log( (Pow(2,self.hypSpace) / delta), 2))
        self.lm = lm
        self.unmasker = pipeline('fill-mask', model=lm)
        self.V = V

        # dynamic
        self.bad_nc = []
        self.bad_pc = []


    def probe(self, sentence):
        # genderPred: 0 = female, 1 = male
        if self.lm.split('-')[0] == 'bert' :
            sentence = sentence.replace('<mask>', '[MASK]')
        result = self.unmasker(sentence)

        for reply in result: # for the replies returned by the language model
            #if female
            if (reply["token_str"]).lower() == "hun" or (reply["token_str"]).lower() == "ho": # i should add more cases
                return 0
            #if male
            if (reply["token_str"]).lower() == "han": # i should add more cases
                return 1
            else:

                continue
        return result[0]['token_str']

    def getRandomValue(self, length, allow_zero):
        vec = list(np.zeros(length, dtype=np.int8))
        # allow for all zeroes: one extra sample length and if its out of index range, use all zeroes vector (equal possibility)
        if allow_zero:
            i = random.randrange(length+1)
        else:
            i = random.randrange(length)
        if i < length:
            vec[i] = 1
        return vec

    def get_label(self, gender, classification):
        """
            Does handling no 1 in vector work as a diverse attribute (neither he or she) to include they?
            -> never gets predicted so what rules result from that? Influences other attributes?
        """
        if (gender[0] == 1 and classification == 0) or (gender[1] == 1 and classification == 1):
            return True
        else:
            return False

    def create_single_sample(self):
        randomVec = []
        for att in self.intepretor.attributes:
            randomVec += self.getRandomValue(self.intepretor.lengths[att], True)
        
        randomGenderVec = self.getRandomValue(2, allow_zero=False)
        randomVec += randomGenderVec

        sentence = self.intepretor.binaryToSentence(randomVec)
        # genderPred: 0 = female, 1 = male
        genderLMPred = self.probe(sentence)
        # if the sampled gender is equal the classification (correctly classified) then we return 1 as 'is valid sentence' 
        # if sampled gender and classification don't match, the sample is not valid and we return 0 as a label
        # label = self.get_label(genderPred, randomGenderVec)
        label = self.get_label(randomGenderVec,genderLMPred)

        return (randomVec,label)
    
    def evalFormula(self, formula, x):
        if formula == true:
            return True
        if formula == false:
            return False
        a = {self.V[i]: x[i] for i in range(len(self.V))}
        for i in range(len(self.V)):
            a[self.V[i]] = (True if x[i] == 1
                            else False)
        return True if formula.subs(a) == True else False
    
    def set2theory(self, set):
        tempt = True
        for e in set:
            tempt = tempt & e
        return tempt
    
    def EQ(self,H):
        h = true
        if len(H):
            h = self.set2theory(H)
        for i in range(self.sampleSize):
            (a,label) = self.create_single_sample()

            # neg counter example
            if label == False and self.evalFormula(h,a) and a not in self.bad_nc:
                # print("neg counterex")
                return (a, i+1)
            # pos counter example
            if label == True and not self.evalFormula(h,a):
                # print("pos counterex")

                return (a, i+1)
        return True
    
    def MQ(self, assignment):
        vec = assignment[:-2]
        genderVec = assignment[-2:]
        sentence = self.intepretor.binaryToSentence(vec)
        genderLMPred = self.probe(sentence)
        label = self.get_label(genderVec, genderLMPred)
        return label
    
    def get_hypothesis(self, S,background):
        H = set()
        for a in [a for a in S if a not in self.bad_nc]:
            L = [self.V[index] for index,value in enumerate(a) if a[index] == 1] + [true]
            R = [self.V[index] for index,value in enumerate(a) if a[index] == 0] + [false]
            for r in R:
                clause = functools.reduce(lambda x,y: x & y, L)
                clause = (clause) >> r
                H.add(clause)
        H = H.union(background)
        return H
    
    def refineHyp(self, H,S,Pos):
        #small optimisation. Refine hypo. with known positive counterexamples.
        for pos in Pos:
            for clause in H.copy():
                if (self.evalFormula(clause, pos) == False):
                    H.remove(clause)

        self.identify_problematic_nc(H,S)
        return H

    def identify_problematic_nc(self, H, S):
        #check if a nc in S does not falsify a clause in H
        h=self.set2theory(H)
        for a in [a for a in S if a not in self.bad_nc]:
            if (self.evalFormula(h, a) == True):
                self.bad_nc.append(a)

    def checkDup(self, list,a):
        if a in list:
            self.bad_nc.append(a)
            return True
        return False
    
    def learn(self,background= {},iterations=-1):
        terminated = False
        metadata = []
        H = set()
        H = H.union(background)
        S = []
        i = 0
        #remember positive counterexamples
        Pos = []
        #list of negative counterexamples that cannot produce a rule (according to positive counterexamples)
        #bad_nc =[]
        while True and iterations!=0:
            data = {}
            start = timeit.default_timer()
            #Ask for H
            eq_res = self.EQ(H)
            if eq_res == True:
                terminated = True
                stop = timeit.default_timer()
                data['runtime'] = stop-start
                metadata.append(data)
                print("terminated")
                # with open('output.txt', 'a') as f:
                #     f.write("=== TERMINATED ===\n")
                return (terminated, metadata, H)

            (counterEx,sampleNr) = eq_res
            data['sample'] = sampleNr
            pos_ex=False

            # if EQ() returns a positive counterexample
            for clause in H.copy():
                if (self.evalFormula(clause, counterEx) == False):
                    if clause in background:
                        self.bad_pc.append(counterEx)
                    else:
                        H.remove(clause)
                        Pos.append(counterEx)
                        self.identify_problematic_nc(H,S)
                        pos_ex = True
                        
            # if EQ() returns a negative counter example
            if not pos_ex:
                replaced = False
                for s in S:
                    s_intersection_x = [1 if s[index] ==1 and counterEx[index] == 1 else 0 for index in range(len(self.V))]
                    A = {index for index,value in enumerate(s_intersection_x) if value ==1}
                    B = {index for index,value in enumerate(s) if value ==1}
                    if A.issubset(B) and not B.issubset(A): # A properly contained in B
                        idx = S.index(s)
                        if self.MQ(s_intersection_x) == False and s_intersection_x not in self.bad_nc:
                            if not self.checkDup(S,s_intersection_x):
                                S[idx] = s_intersection_x
                                replaced = True
                            break
                if not replaced:
                    S.append(counterEx)

                H = self.get_hypothesis(S,background)
                H = self.refineHyp(H,S,Pos)

            # logging
            iterations-=1
            stop = timeit.default_timer()
            data['runtime'] = stop-start
            metadata.append(data)
            i += 1
            print(f"iteration = {i}, len(H) = {len(H)}, runTime = {[data['runtime']]}")

            # if iterations % 5 == 0:
            #     log = f"iteration = {i}, len(H) = {len(H)}, rt = {[data['runtime']]}"
            #     with open('output.txt', 'a') as f:
            #         f.write(log)
        return (terminated, metadata, H)
