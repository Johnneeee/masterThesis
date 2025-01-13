import functools
import random
import timeit
from math import prod
import numpy as np
from sympy import true, false, Pow, log #using sympy's log and pow to avoid overflow
from intepretor import Intepretor # just for pretty syntax
from transformers import pipeline
from tqdm import tqdm

# Helper functions for the Horn algorithm
def getRandomValue(length, allow_zero):
    vec = list(np.zeros(length, dtype=np.int8))
    # allow for all zeroes: one extra sample length and if its out of index range, use all zeroes vector (equal possibility)
    if allow_zero:
        i = random.randrange(length+1)
    else:
        i = random.randrange(length)
    if i < length:
        vec[i] = 1
    return vec

def set2formula(set): #converting set of sympy formulas to one big sympy formula 
    finalFormula = True
    for formula in set:
        finalFormula &= formula
    return finalFormula

# epsilon = # error: (differ between model and sampled)
# delta = # confidence: (chance of differ)
class HornAlgorithm():                                                          
    def __init__(self, langaugeModel : str, intepretor : Intepretor, vocabulary, triggerTokens, epsilon = 0.2, delta = 0.1):
        # static
        self.intepretor = intepretor
        self.hypSpace = prod(self.intepretor.lengths.values())*2
        self.sampleSize = int ( (1/epsilon) * log( (Pow(2,self.hypSpace) / delta), 2))
        self.unmasker = pipeline('fill-mask', model=langaugeModel)
        self.V = vocabulary
        self.femaleTokens = triggerTokens[0]
        self.maleTokens = triggerTokens[1]
        # dynamic
        self.bad_nc = [] # list of negative counterexamples that cannot produce a rule (according to positive counterexamples)
        self.bad_pc = []

    def probe(self, sentence : str):
        result = self.unmasker(sentence)

        for reply in result: # for the replies returned by the language model
            token = (reply["token_str"]).lower()
            #if female
            if token in self.femaleTokens:
                return [1,0]
            #if male
            if token in self.maleTokens:
                return [0,1]

        return [0,0]

    def generate_sample(self):
        generatedVec = []
        for att in self.intepretor.attributes:
            generatedVec += getRandomValue(self.intepretor.lengths[att], True) #why true
        generatedGender = getRandomValue(2, False)
        generatedVec += generatedGender

        sentence = self.intepretor.binaryToSentence(generatedVec)
        predictedGender = self.probe(sentence)

        label = generatedGender == predictedGender
        return (generatedVec,label)
    
    def evalFormula(self, formula, vector): # -> bool
        if formula in {true, false}:
            return formula
        
        d = {} # {symbol: bool} # setup for .subs
        for i in range(len(self.V)):
            d[self.V[i]] = vector[i] == 1

        return formula.subs(d)  # .subs does the evaluation, given the formula and its truth values per symbol
    
    def EQ(self,H):
        h = set2formula(H) if len(H) else true # convert h to big formula

        for sampleNr in range(1,self.sampleSize+1):
            (generatedVec,label) = self.generate_sample()
            evaluatedTheory = self.evalFormula(h,generatedVec)

            # pos counterExample(for mange)
            if label == False and evaluatedTheory and (generatedVec not in self.bad_nc):
                return (generatedVec, sampleNr)
            
            # neg counterExample (for få)
            if label == True and evaluatedTheory == False:
                return (generatedVec, sampleNr)

        return (True,0)
    
    def MQ(self, assignment):
        vec = assignment[:-2] # excluding genders
        sentence = self.intepretor.binaryToSentence(vec)

        generatedGender = assignment[-2:]
        predictedGender = self.probe(sentence)
        
        return generatedGender == predictedGender
    
    def get_hypothesis(self, S):
        H = set()
        sFiltered = list(filter(lambda x: x not in self.bad_nc, S)) # [vec]

        for vec in sFiltered:
            L = [self.V[i] for i,val in enumerate(vec) if val == 1] + [true] # vec -> true(vec)
            R = [self.V[i] for i,val in enumerate(vec) if val == 0] + [false] # vec -> false(vec)
            for r in R:
                clause = functools.reduce(lambda x,y: x & y, L) #[symbols] -> &symbols
                clause = (clause) >> r # clause = Implies(clause,r)
                H.add(clause)
        return H

    def refineHyp(self, H : set, posCounterEx):
        #small optimisation. Refine hypo. with known positive counterexamples.
        refined_h = H.copy()

        for clause in H:
            for vec in posCounterEx:
                if self.evalFormula(clause, vec) == False:
                    refined_h.remove(clause)
                    break

        return refined_h

    # bad_nc is the implicated pos counter examples??
    def find_bad_nc(self, H, S): 
        #check if a nc in S does not falsify a clause in H
        h = set2formula(H)
        sFiltered = list(filter(lambda x: x not in self.bad_nc, S)) # [vec]
        for vec in sFiltered:
            if (self.evalFormula(h, vec) == True):
                self.bad_nc.append(vec)
    
    def learn(self,iterationCap,background = set()):
        metadata = [] #[[iteration, len(H), sampleNr, runtime]]
        H = background
        S = []
        #remember positive counterexamples
        posCounterEx = []

        for iteration in tqdm(range(1,iterationCap+1), desc="Eq iteration"):
            start = timeit.default_timer()

            (counterEx,sampleNr) = self.EQ(H)

            if counterEx == True: #if eq -> True
                # logging metadata
                metadata.append([iteration, len(H), "TRUE", round(timeit.default_timer()-start, 3)])
                return (metadata, H)

            pos_ex=False # posEx/negEx lock

            for clause in H.copy(): # if (eq -> positive counter example)

                if clause in background: # quick exit check
                    self.bad_pc.append(counterEx)
                    continue

                if (self.evalFormula(clause, counterEx) == False):
                    H.remove(clause)
                    posCounterEx.append(counterEx)
                    self.find_bad_nc(H,S)
                    pos_ex = True
                        
            if pos_ex == False: # else (eq -> negative counter example)
                for i, s in enumerate(S): # if (exists s in S s.t. statements)
                    cap_sc = [1 if (s[i] ==1 and counterEx[i] == 1) else 0 for i in range(len(self.V))] # cap = intersection
                    true_sc = {i for i,val in enumerate(cap_sc) if val == 1}
                    true_s = {i for i,val in enumerate(s) if val == 1}

                    if cap_sc in S:
                        self.bad_nc.append(cap_sc)

                    if cap_sc in self.bad_nc: # quick exit check
                        continue

                    if true_sc.issubset(true_s) and (true_s.issubset(true_sc) == False): # if (s \cap c) \subset s
                        if self.MQ(cap_sc) == False: # if mq(s \cap c) = "no"
                            S[i] = cap_sc
                            break

                else: # else (doesnt exists s in S s.t. statements)
                    S.append(counterEx)

                H = self.get_hypothesis(S).union(background)
                H = self.refineHyp(H,posCounterEx)
                self.find_bad_nc(H,S)

            # logging metadata
            metadata.append([iteration, len(H), sampleNr, round(timeit.default_timer()-start, 3)])

        return (metadata, H)
