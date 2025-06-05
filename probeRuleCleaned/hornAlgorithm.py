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
def divideV(intepretor: Intepretor, V):
    splitIndexes = []
    i = 0
    for x in intepretor.lengths.items():
        splitIndexes.append((i,x[1] + i))
        i += x[1]

    splitIndexes.append((i,len(V)))
    available = [V[s:e] for s,e in splitIndexes]
    return available

def getRandomValue(length, allow_zero):
    vec = list(np.zeros(length, dtype=np.int8))
    i = random.randrange(length+1) if allow_zero else random.randrange(length) # zero vector if random i > length
    if i < length: vec[i] = 1 #if known value is chosen
    return vec

def set2formula(set): #converting set of sympy formulas to one big sympy formula 
    return functools.reduce(lambda x,y: x & y, set | {True}) # {sympy} -> &sympy & True

# epsilon = # error: (differ between model and sampled)
# delta = # confidence: (chance of differ)
class HornAlgorithm():                                                          
    def __init__(self,intepretor : Intepretor, vocabulary, triggerTokens, langaugeModel : str, epsilon = 0.2, delta = 0.1):
        # static
        self.intepretor = intepretor
        self.V = vocabulary
        self.femaleTokens = triggerTokens[0]
        self.maleTokens = triggerTokens[1]

        self.hypSpace = prod(self.intepretor.lengths.values())*2
        self.sampleSize = int ( (1/epsilon) * log( (Pow(2,self.hypSpace) / delta), 2))
        self.unmasker = pipeline('fill-mask', model=langaugeModel)
        self.Vsections = divideV(intepretor, vocabulary)

        # dynamic
        self.bad_nc = [] # list of negative counterexamples that cannot produce a rule (according to positive counterexamples)

    def probe(self, sentence : str):
        for reply in self.unmasker(sentence): # for the replies returned by the language model
            token = (reply["token_str"]).lower()
            if token in self.femaleTokens: return [1,0] # if female
            if token in self.maleTokens: return [0,1]   # if male
        return [0,0]

    def generate_sample(self):
        vec = sum([getRandomValue(self.intepretor.lengths[att], True) for att in self.intepretor.attributes],[]) # generating random vector
        genderVec = getRandomValue(2, False)
        vec += genderVec # random vector + random gender
        predGenderVec = self.probe(self.intepretor.binaryToSentence(vec))
        if predGenderVec == [0,0]:
            self.bad_nc.append(vec)
        return (vec,genderVec == predGenderVec) #(vector, label)
    
    def evalFormula(self, formula, vector): # -> bool
        if formula in {true, false}: return formula
        
        d = {} # {symbol: bool} # setup for .subs
        for i in range(len(self.V)):
            d[self.V[i]] = vector[i] == 1

        return formula.subs(d)  # .subs does the evaluation, given the formula and its truth values per symbol
    
    def EQ(self,H):
        h = set2formula(H) # convert h to big formula

        for sampleNr in range(1,self.sampleSize+1):
            (generatedVec,label) = self.generate_sample()
            evaluatedTheory = self.evalFormula(h,generatedVec)

            # neg counterExample (too few)
            # ex = (car -> pink): h = (plane -> red) -> (plane -> red), (car -> pink)
            if label == False and evaluatedTheory and (generatedVec not in self.bad_nc):
                return (generatedVec, sampleNr)
            
            # pos counterExample (too many)
            # ex = (car -> blue): h = (car -> red), (car -> blue) -> h = (car -> blue)
            if label == True and evaluatedTheory == False:
                return (generatedVec, sampleNr)

        return (True,0)
    
    def MQ(self, assignment):
        vec, genderVec = assignment[:-2], assignment[-2:]
        sentence = self.intepretor.binaryToSentence(vec)
        return genderVec == self.probe(sentence)
    
    def get_hypothesis(self, S):
        H = set()
        sFiltered = list(filter(lambda x: x not in self.bad_nc, S)) # [vec]
        for vec in sFiltered:
            L = [self.V[i] for i,val in enumerate(vec) if val == 1] + [true]    # vec -> true(vec)
            R = sum(list(filter(lambda x: (set(L) & set(x)) == set(), self.Vsections)),[]) + [false] # filters away unavailable "categories"
            
            ant = functools.reduce(lambda x,y: x & y, L) #[symbols] -> &symbols
            for con in R:
                rule = (ant) >> con # clause = Implies(ant,con)
                H.add(rule)

        return H

    def find_bad_nc(self, H, S): # append s to bad_nc if s in S does not falsify H
        h = set2formula(H)
        for vec in S:
            if ((vec not in self.bad_nc) and (self.evalFormula(h, vec) == True)):
                self.bad_nc.append(vec)
    
    def learn(self,iterationCap,background = set()):
        metadata = [] #[[iteration, len(H), sampleNr, runtime(sample), runtime(total)]]
        posCounterEx = [] #tracks positive counterexamples encountered
        
        H = background
        S = []

        # try:
        for iteration in tqdm(range(1,iterationCap+1), desc="Eq iteration"):
            start = timeit.default_timer()
            (counterEx,sampleNr) = self.EQ(H)

            if counterEx == True: #if (eq -> True)
                metadata.append([iteration, len(H), "TRUE", f"{timeit.default_timer()-start:.3f}"]) # logging metadata
                return (metadata, H, iteration)

            pos_ex=False # posEx/negEx lock

            for clause in H.copy(): # if (eq -> positive counter example)
                if ((clause not in background) and (self.evalFormula(clause, counterEx) == False)):
                    H.remove(clause)
                    pos_ex = True

            if pos_ex: posCounterEx.append(counterEx) # if counterexample confirmed as positive counterexample

            if pos_ex == False: # else (eq -> negative counter example)
                for idx, s in enumerate(S): # if (exists s in S s.t. statements)
                    cap_sc = [1 if (s[i] == 1 and counterEx[i] == 1) else 0 for i in range(len(self.V))] # cap = intersection
                    true_sc = {i for i,val in enumerate(cap_sc) if val == 1}
                    true_s = {i for i,val in enumerate(s) if val == 1}

                    if cap_sc in self.bad_nc: continue # quick exit check
                    if cap_sc in S: # quick exit check (this happens less often)
                        self.bad_nc.append(cap_sc)
                        continue

                    if true_sc.issubset(true_s) and (true_s.issubset(true_sc) == False): # if (s \cap c) \subset s
                        if self.MQ(cap_sc) == False: # if mq(s \cap c) = "no"
                            S[idx] = cap_sc
                            break

                else: S.append(counterEx) # else (doesnt exists s in S s.t. statements)

                H = self.get_hypothesis(S).union(background)
                H = set(filter(lambda x: all(self.evalFormula(x, vec) for vec in posCounterEx), H.copy())) # refining H: drops h in H where exsists p in P s.t. p falsifies h

            self.find_bad_nc(H,S)
            metadata.append([iteration, len(H), sampleNr, f"{timeit.default_timer()-start:.3f}"]) # logging metadata
        return (metadata, H, iteration)
        # except: # save current data in case user decides to interupt the run
        #     return (metadata, H, iteration-1) # -1 to match the counting bar which starts at 0
