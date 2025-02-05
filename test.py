# # import functools
# # import random
# # import timeit
# # from math import prod
# # import numpy as np
# # from sympy import true, false, Pow, log #using sympy's log and pow to avoid overflow
# # from intepretor import Intepretor # just for pretty syntax
# # from transformers import pipeline
# # from tqdm import tqdm

# # # Helper functions for the Horn algorithm
# # def getRandomValue(length, allow_zero):
# #     vec = list(np.zeros(length, dtype=np.int8))
# #     # allow for all zeroes: one extra sample length and if its out of index range, use all zeroes vector (equal possibility)
# #     if allow_zero:
# #         i = random.randrange(length+1)
# #     else:
# #         i = random.randrange(length)
# #     if i < length:
# #         vec[i] = 1
# #     return vec

# # def set2formula(set): #converting set of sympy formulas to one big sympy formula 
# #     finalFormula = True
# #     for formula in set:
# #         finalFormula &= formula
# #     return finalFormula

# # # epsilon = # error: (differ between model and sampled)
# # # delta = # confidence: (chance of differ)
# # class HornAlgorithm():                                                          
# #     def __init__(self,intepretor : Intepretor, vocabulary, triggerTokens, langaugeModel : str, epsilon = 0.2, delta = 0.1):
# #         # static
# #         self.intepretor = intepretor
# #         self.hypSpace = prod(self.intepretor.lengths.values())*2
# #         self.sampleSize = int ( (1/epsilon) * log( (Pow(2,self.hypSpace) / delta), 2))
# #         self.unmasker = pipeline('fill-mask', model=langaugeModel)
# #         self.V = vocabulary
# #         self.femaleTokens = triggerTokens[0]
# #         self.maleTokens = triggerTokens[1]
# #         # dynamic
# #         self.bad_nc = [] # list of negative counterexamples that cannot produce a rule (according to positive counterexamples)
# #         self.bad_pc = []
# #         self.posCounterEx = [] #tracks positive counterexamples encountered

# #     def probe(self, sentence : str):
# #         result = self.unmasker(sentence)

# #         for reply in result: # for the replies returned by the language model
# #             token = (reply["token_str"]).lower()
# #             #if female
# #             if token in self.femaleTokens:
# #                 return [1,0]
# #             #if male
# #             if token in self.maleTokens:
# #                 return [0,1]

# #         return [0,0]

# #     def generate_sample(self):
# #         generatedVec = []
# #         for att in self.intepretor.attributes:
# #             generatedVec += getRandomValue(self.intepretor.lengths[att], True) #why true
# #         generatedGender = getRandomValue(2, False)
# #         generatedVec += generatedGender

# #         sentence = self.intepretor.binaryToSentence(generatedVec)
# #         predictedGender = self.probe(sentence)

# #         label = generatedGender == predictedGender
# #         return (generatedVec,label)

# #     def evalFormula(self, formula, vector): # -> bool
# #         if formula in {true, false}:
# #             return formula

# #         d = {} # {symbol: bool} # setup for .subs
# #         for i in range(len(self.V)):
# #             d[self.V[i]] = vector[i] == 1

# #         return formula.subs(d)  # .subs does the evaluation, given the formula and its truth values per symbol

# #     def EQ(self,H):
# #         h = set2formula(H) if len(H) else true # convert h to big formula

# #         for sampleNr in range(1,self.sampleSize+1):
# #             (generatedVec,label) = self.generate_sample()
# #             evaluatedTheory = self.evalFormula(h,generatedVec)

# #             # pos counterExample(for mange)
# #             if label == False and evaluatedTheory and (generatedVec not in self.bad_nc):
# #                 return (generatedVec, sampleNr)

# #             # neg counterExample (for få)
# #             if label == True and evaluatedTheory == False:
# #                 return (generatedVec, sampleNr)

# #         return (True,0)

# #     def MQ(self, assignment):
# #         vec = assignment[:-2] # excluding genders
# #         sentence = self.intepretor.binaryToSentence(vec)

# #         generatedGender = assignment[-2:]
# #         predictedGender = self.probe(sentence)

# #         return generatedGender == predictedGender

# #     def get_hypothesis(self, S):
# #         H = set()
# #         sFiltered = list(filter(lambda x: x not in self.bad_nc, S)) # [vec]

# #         for vec in sFiltered:
# #             L = [self.V[i] for i,val in enumerate(vec) if val == 1] + [true] # vec -> true(vec)
# #             R = [self.V[i] for i,val in enumerate(vec) if val == 0] + [false] # vec -> false(vec)
# #             for r in R:
# #                 clause = functools.reduce(lambda x,y: x & y, L) #[symbols] -> &symbols
# #                 clause = (clause) >> r # clause = Implies(clause,r)
# #                 H.add(clause)
# #         return H

# #     def refineHyp(self, H : set):
# #         # drops h in H where exsists p in P s.t. p falsifies h
# #         refined_h = set(filter(lambda x: all(self.evalFormula(x, vec) for vec in self.posCounterEx), H.copy()))
# #         return refined_h

# #     # bad_nc is the implicated pos counter examples??
# #     def find_bad_nc(self, H, S): 
# #         #check if a nc in S does not falsify a clause in H
# #         h = set2formula(H)
# #         sFiltered = list(filter(lambda x: x not in self.bad_nc, S)) # [vec]
# #         for vec in sFiltered:
# #             if (self.evalFormula(h, vec) == True):
# #                 self.bad_nc.append(vec)

# #     def learn(self,iterationCap,background = set()):
# #         metadata = [] #[[iteration, len(H), sampleNr, runtime]]
# #         H = background
# #         S = []

# #         # try:
# #         for iteration in tqdm(range(1,iterationCap+1), desc="Eq iteration"):
# #             start = timeit.default_timer()

# #             (counterEx,sampleNr) = self.EQ(H)
# #             if counterEx == True: #if eq -> True
# #                 metadata.append([iteration, len(H), "TRUE", round(timeit.default_timer()-start, 3)]) # logging metadata
# #                 return (metadata, H, iteration)

# #             pos_ex=False # posEx/negEx lock

# #             for clause in H.copy(): # if (eq -> positive counter example)

# #                 if clause in background: # quick exit check
# #                     # self.bad_pc.append(counterEx)
# #                     continue

# #                 if (self.evalFormula(clause, counterEx) == False):
# #                     H.remove(clause)
# #                     pos_ex = True

# #             if pos_ex: # if counterexample confirmed as positive counterexample
# #                 self.posCounterEx.append(counterEx)

# #             if pos_ex == False: # else (eq -> negative counter example)
# #                 for idx, s in enumerate(S): # if (exists s in S s.t. statements)
# #                     cap_sc = [1 if (s[i] == 1 and counterEx[i] == 1) else 0 for i in range(len(self.V))] # cap = intersection
# #                     true_sc = {i for i,val in enumerate(cap_sc) if val == 1}
# #                     true_s = {i for i,val in enumerate(s) if val == 1}

# #                     if cap_sc in S: # quick exit check
# #                         self.bad_nc.append(cap_sc)
# #                         continue

# #                     if cap_sc in self.bad_nc: # quick exit check
# #                         continue

# #                     if true_sc.issubset(true_s) and (true_s.issubset(true_sc) == False): # if (s \cap c) \subset s
# #                         if self.MQ(cap_sc) == False: # if mq(s \cap c) = "no"
# #                             S[idx] = cap_sc
# #                             break

# #                 else: # else (doesnt exists s in S s.t. statements)
# #                     S.append(counterEx)

# #                 H = self.get_hypothesis(S).union(background)
# #                 H = self.refineHyp(H)

# #             self.find_bad_nc(H,S)
# #             metadata.append([iteration, len(H), sampleNr, round(timeit.default_timer()-start, 3)]) # logging metadata
# #         return (metadata, H, iteration)
# #         # except: # save current data in case user decides to interupt the run
# #         #     return (metadata, H, iteration-1) # -1 to match the counting bar which starts at 0

        

# # import sympy

# # print(sympy.diff(("a","b","c"),("a","d","e")))

# # x = {"apple", "banana", "cherry"}
# # y = {"google", "microsoft", "apple"}




# # a = {{"Afrika", "Stavanger"}, "FALSE"}
# # b = {{"Stavanger", "Afrika"}, "FALSE"} 

# # diff = a.symmetric_difference(b)
# # print(diff)

# # print(z)

# # print(type(("Afrika","Stavanger")))


# # a = {{'kvinne', 'mellom 30 og 40', 'sveiser', 'Stavanger'}, 'FALSE\n'}
# # b = {{'mellom 30 og 40','kvinne','Stavanger', 'sveiser'}, 'FALSE\n'}

# # print(a == b)

# # print(({"Afrika","Stavanger"}, ("eldre enn 60")) == ({"Stavanger", "Afrika"}, ("eldre enn 60")))
# # Stavanger & Afrika ---> eldre enn 60 (norbert) !=
# # Afrika & Stavanger ---> eldre enn 60 (norbert2)
# # [(Afrika,Stavanger), (eldre enn 60)] (norbert2)

# ### until 11.02 11:15
# # for lm in lms:
#     # countRules(f"{lm}_i100", [f"{lm}_{x}" for x in eq100], [1,1,1]) !!!!!!!!!!!!!!!!!!!
#     # countRules(f"{lm}_i200", [f"{lm}_{x}" for x in eq200], [1,1]) !!!!!!!!!!!!!!!
#     # countRules(f"{lm}_iAll(weighted)", [f"{lm}_{x}" for x in eq100 + eq200 + eq300], [1,1,1,2,2,3])

# # compare all models, compare agreement for 100/200/300. goal == if more agreement if more iteration
# # top x(5?) rules for 100/200/300
# # find the model that the other models agrees more. (voting method)
# # sym diff 300 (a,b,c) (a,d,e) = (b,c,d,e)

# # run 

# #   a b c d e f g
# # a 0
# # b   0
# # c     0
# # d       0
# # e         0
# # f           0
# # g             0
# # 11.02.25 11:15

# # woman & elektriker -> Oslo (in norbert) agreement with other models?

# # woman & elektriker -> false (in norbert)
# # true in probing?


# # cities = ['Oslo', 'Kristiansand', 'Stavanger', 'Bergen', 'Ålesund', 'Trondheim', 'Bodø', 'Tromsø']
# # eth = ['Asia', 'Afrika', 'Nord Amerika', 'Sør Amerika', 'Europa', 'Australia']

# # data = [['Bergen ---> mann'], ['Bodø ---> mann'], ['Nord Amerika & mellom 40 og 50 ---> mann'], ['Nord Amerika & mellom 40 og 50 ---> rørlegger'], ['Stavanger & Afrika ---> eldre enn 60'], ['Stavanger & Afrika ---> mann'], ['Stavanger & Afrika ---> sveiser'], ['mann & sykepleier ---> Afrika'], ['mann & sykepleier ---> yngre enn 20'], ['sveiser & kvinne ---> Asia'], ['sveiser & kvinne ---> Stavanger'], ['yngre enn 20 & kvinne ---> sykepleier'], ['Kristiansand & Nord Amerika & mann & mellom 50 og 60 & frisør ---> FALSE'], ['Oslo & Australia & mann & psykolog ---> FALSE'], ['arkitekt & Trondheim & kvinne ---> FALSE'], ['elektriker & kvinne ---> FALSE'], ['kvinne & eldre enn 60 ---> FALSE'], ['mellom 30 og 40 & Europa ---> FALSE'], ['politiker & kvinne ---> FALSE']]

# # for i in range(len(data)):
# #     for x in cities:
# #         data[i] = [data[i][0].replace(x,f"{x}(stay)")]
# #     for x in eth:
# #         data[i] = [data[i][0].replace(x,f"{x}(ethnicity)")]

# # print(data)
# # importing libraries
# import matplotlib.pyplot as plt
# import numpy as np
# import math

# # Get the angles from 0 to 2 pie (360 degree) in narray object
# X = np.arange(0, math.pi*2, 0.05)
# # Using built-in trigonometric function we can directly plot
# # the given cosine wave for the given angles
# Y1 = np.sin(X)
# Y2 = np.cos(X)
# Y3 = np.tan(X)
# Y4 = np.tanh(X)

# # Initialise the subplot function using number of rows and columns

# from math import log

# h100 = ['102', '118', '92', '89', '88', '88', '95', '117', '97', '98', '114', '136', '143', '150', '130', '127', '145', '152', '149', '130', '126', '142', '143', '163', '140', '141', '138', '147', '153', '162', '158', '146', '145', '159', '168', '169', '169', '170', '184', '164', '153', '149', '161', '177', '190', '189', '188', '175', '174', '175', '176', '157', '158', '159', '160', '158', '155', '167', '165', '163', '169', '168', '182', '198', '205', '188', '189', '175', '182', '183', '190', '179', '176', '167', '184', '191', '194', '191', '187', '184', '181', '167', '181', '178', '185', '184', '190', '183', '196', '189', '189', '188', '189', '182', '191', '192', '210', '191', '192', '204']
# h200 = ['88', '89', '105', '91', '93', '88', '112', '113', '133', '116', '95', '91', '92', '106', '107', '115', '139', '141', '120', '133', '129', '130', '119', '116', '128', '136', '115', '128', '125', '115', '112', '113', '116', '116', '123', '129', '130', '138', '139', '140', '139', '137', '146', '147', '165', '181', '180', '179', '177', '190', '198', '205', '211', '198', '206', '201', '202', '199', '183', '190', '191', '190', '189', '195', '197', '191', '192', '189', '196', '195', '175', '172', '179', '176', '173', '185', '188', '181', '178', '159', '159', '161', '160', '161', '159', '160', '182', '162', '171', '162', '163', '165', '171', '170', '169', '166', '159', '168', '175', '164', '165', '163', '179', '177', '172', '158', '156', '155', '154', '160', '161', '174', '181', '172', '173', '182', '174', '175', '176', '198', '214', '200', '181', '180', '177', '192', '194', '201', '190', '189', '190', '197', '199', '195', '204', '191', '193', '186', '185', '186', '188', '187', '185', '182', '179', '180', '195', '191', '190', '188', '196', '205', '211', '211', '189', '204', '210', '211', '221', '230', '229', '230', '239', '241', '247', '238', '245', '254', '233', '231', '238', '239', '236', '229', '236', '237', '243', '255', '268', '268', '275', '276', '267', '268', '277', '276', '269', '270', '271', '280', '278', '279', '293', '284', '283', '301', '300', '306', '289', '288']
# h300 = ['88', '116', '89', '88', '88', '102', '108', '109', '110', '112', '94', '92', '101', '123', '124', '125', '147', '171', '167', '168', '146', '168', '175', '185', '195', '180', '177', '192', '205', '206', '207', '187', '197', '199', '207', '203', '200', '207', '203', '210', '223', '238', '219', '216', '223', '230', '232', '245', '231', '239', '219', '199', '196', '182', '183', '183', '170', '169', '166', '168', '165', '164', '179', '186', '185', '193', '201', '188', '185', '174', '175', '182', '188', '190', '169', '170', '169', '168', '165', '147', '143', '140', '129', '127', '129', '135', '136', '133', '148', '157', '150', '148', '149', '155', '175', '183', '181', '197', '197', '196', '201', '188', '188', '189', '190', '190', '191', '207', '208', '209', '196', '197', '198', '199', '202', '198', '180', '192', '190', '191', '176', '178', '177', '190', '191', '192', '190', '192', '201', '203', '212', '213', '214', '206', '192', '206', '202', '209', '210', '223', '214', '215', '216', '218', '216', '214', '215', '222', '234', '232', '241', '229', '216', '217', '233', '247', '254', '251', '250', '249', '250', '247', '246', '245', '246', '244', '250', '266', '267', '280', '269', '260', '270', '256', '258', '258', '267', '265', '266', '284', '273', '271', '267', '258', '256', '257', '257', '258', '265', '280', '300', '296', '303', '304', '311', '318', '319', '305', '314', '316', '314', '315', '299', '298', '305', '304', '300', '307', '307', '305', '303', '302', '303', '313', '312', '313', '311', '311', '313', '312', '301', '300', '294', '296', '297', '285', '287', '280', '300', '299', '297', '298', '299', '306', '305', '298', '307', '306', '289', '288', '300', '300', '294', '274', '273', '282', '281', '282', '283', '282', '291', '277', '275', '275', '284', '285', '284', '291', '290', '291', '290', '286', '285', '292', '291', '301', '303', '302', '310', '311', '309', '310', '311', '320', '321', '313', '312', '321', '321', '321', '330', '330', '328', '329', '344', '345', '351', '342', '351', '352', '366', '373', '354', '338', '340', '349', '363', '364', '363', '362']

# h100 = [float(x) for x in h100]
# h200 = [float(x) for x in h200]
# h300 = [float(x) for x in h300]

# s100 = ['1', '4', '1', '3', '2', '2', '7', '2', '2', '2', '1', '1', '4', '2', '1', '2', '7', '1', '2', '6', '3', '2', '1', '4', '1', '3', '3', '1', '1', 
# '2', '10', '1', '1', '3', '2', '1', '5', '2', '1', '1', '3', '1', '3', '1', '2', '1', '4', '1', '2', '1', '3', '2', '3', '1', '2', '4', '4', '8', 
# '1', '4', '3', '4', '6', '3', '2', '4', '2', '1', '1', '9', '2', '3', '4', '1', '4', '1', '2', '5', '1', '5', '1', '1', '7', '2', '2', '5', '1', '3', '9', '1', '1', '1', '4', '1', '2', '2', '4', '3', '9', '3']
# s200 = ['1', '1', '1', '2', '6', '1', '2', '1', '1', '1', '1', '4', '1', '1', '9', '1', '1', '6', '3', '4', '1', '3', '1', '1', '3', '4', '2', '4', '2', 
# '1', '1', '4', '1', '4', '3', '1', '1', '5', '3', '7', '1', '1', '3', '3', '8', '3', '4', '3', '4', '1', '3', '1', '8', '1', '2', '3', '5', '2', '2', '3', '3', '1', '3', '8', '3', '11', '2', '6', '5', '4', '2', '1', '1', '2', '3', '6', '2', '1', '27', '16', '2', '2', '5', '5', '3', '2', '7', '1', '1', '3', '10', '1', '9', '5', '4', '5', '5', '2', '3', '1', '3', '4', '9', '5', '2', '1', '2', '5', '2', '9', '3', '6', '1', '13', '1', '1', '4', '2', '1', '3', '1', '3', '7', '19', '7', '2', '1', '7', '16', '6', '4', '3', '18', '3', '9', '1', '2', '4', '4', '10', '6', '3', '3', '11', '7', '6', '1', '3', '1', '7', '1', '5', '4', '9', '3', '1', '4', '2', '2', '5', '6', '12', '7', '4', '10', '2', '12', '1', '4', '1', '2', '2', '3', '1', '6', '2', '1', '5', '1', '13', '8', '1', '10', '10', '1', '5', '2', '1', '2', '6', '4', '4', '2', '3', '6', '2', '4', '3', '3', '3']
# s300 = ['2', '1', '4', '3', '2', '1', '1', '1', '2', '2', '2', '2', '1', '1', '2', '7', '2', '7', '1', '2', '1', '1', '4', '10', '1', '1', '1', '3', '3', '6', '1', '2', '7', '1', '1', '3', '8', '6', '4', '1', '2', '1', '4', '5', '8', '4', '3', '4', '10', '4', '1', '4', '9', '3', '2', '1', '10', '2', '2', '2', '2', '1', '1', '7', '7', '2', '2', '1', '3', '1', '12', '2', '1', '3', '1', '3', '6', '1', '1', '2', '2', '6', '1', '8', '7', '2', '1', '1', '3', '1', '3', '3', '1', '3', '2', '2', '1', '2', '1', '1', '1', '2', '6', '2', '4', '1', '1', '2', '3', '2', '9', '2', '4', '7', '4', '2', '8', '2', '1', '3', '1', '5', '2', '1', '3', '6', '3', '1', '2', '1', '17', '1', '4', '3', '6', '1', '6', '3', '16', '14', '1', '2', '1', '6', '2', '1', '4', '5', '5', '1', '8', '2', '4', '3', '2', '2', '7', '11', '1', '1', '6', '2', '5', '6', '2', '1', '9', '4', '8', '4', '7', '3', '2', '2', '3', '2', '2', '1', '7', '3', '3', '2', '3', '2', '3', '3', '1', '1', '1', '2', '1', '1', '1', '7', '9', '4', '4', '1', '8', '3', '1', '3', '4', '3', '9', '14', '4', '3', '1', '3', '1', '6', '7', '1', '14', '1', '1', '4', '5', '2', '2', '1', '3', '5', '1', '2', '4', '9', '1', '2', '3', '2', '5', '9', '1', '3', '18', '4', '5', '3', '6', '5', '1', '4', '1', '8', '2', '2', '2', '15', '9', '1', '3', '3', '10', '3', '2', '2', '2', '12', '4', '2', '3', '5', '3', '4', '5', '1', '2', '3', '7', '12', '7', '3', '5', '4', '1', '3', '1', '6', '4', '2', '1', '6', '1', '1', '15', '2', '1', '4', '8', '3', '3', '14', '1', '1', '5', '3', '4', '15']

# s100 = [int(x) for x in s100]
# s200 = [int(x) for x in s200]
# s300 = [int(x) for x in s300]

# r100 = ['1.091', '2.195', '0.418', '1.100', '0.894', '1.672', '4.327', '2.268', '1.454', '2.245', '2.201', '2.487', '4.060', '3.981', '3.166', '2.278', '5.684', '3.360', '2.579', '4.134', '2.598', '3.499', '3.203', '4.865', '1.810', '4.272', '4.576', '3.714', '4.139', '4.758', '6.344', '4.411', '2.171', '5.666', '5.333', '5.156', '7.151', '6.169', '5.812', '3.177', '6.989', '2.893', '6.452', '5.960', '6.658', '3.516', '5.127', '6.769', '3.918', '6.754', '8.498', '4.052', '8.979', '7.679', '8.102', '5.659', '9.269', '11.264', '3.918', '5.479', '9.511', '9.461', '10.483', '9.805', '9.892', '10.058', '9.723', '8.616', '8.640', '13.395', '10.753', '10.376', '6.026', '8.648', '10.685', '11.096', '11.160', '7.291', '10.773', '6.545', '4.584', '4.452', '14.547', '5.246', '11.762', '7.196', '12.074', '14.292', '15.506', '11.882', '11.806', '11.283', '13.520', '11.084', '11.175', '11.991', '13.537', '5.924', '16.363', '13.868']
# r200 = ['0.929', '1.295', '1.369', '1.556', '3.466', '0.836', '1.931', '1.519', '1.927', '1.933', '1.082', '2.316', '1.565', '1.973', '5.759', '2.309', '2.550', '4.965', '2.394', '3.955', '1.714', '3.639', '2.924', '1.574', '4.234', '4.727', '2.117', '4.690', '2.322', '3.612', '1.664', '4.617', '3.658', '4.535', '4.384', '3.897', '4.148', '6.090', '5.886', '7.524', '2.601', '2.575', '5.830', '6.639', '9.179', '7.462', '8.160', '4.497', '5.153', '6.381', '7.914', '7.042', '11.261', '7.259', '7.936', '8.663', '10.168', '4.665', '4.416', '9.022', '10.073', '4.479', '9.771', '11.875', '9.763', '9.282', '10.158', '12.184', '12.361', '11.334', '4.857', '4.168', '10.695', '5.088', '10.997', '12.771', '10.686', '10.122', '17.470', '11.069', '9.990', '10.053', '5.572', '11.801', '10.179', '9.599', '13.599', '3.528', '10.179', '10.991', '13.970', '10.184', '13.796', '5.841', '5.655', '12.497', '13.057', '11.110', '11.869', '4.527', '13.208', '5.897', '16.048', '6.686', '12.411', '4.136', '4.704', '5.861', '11.867', '15.028', '11.898', '14.719', '12.945', '18.695', '12.757', '12.309', '14.410', '14.509', '14.809', '15.195', '15.330', '6.761', '8.345', '14.151', '7.991', '16.013', '15.716', '20.388', '13.397', '8.128', '18.842', '18.994', '25.869', '7.262', '22.072', '18.448', '19.424', '7.926', '7.806', '24.319', '21.430', '19.530', '7.537', '23.588', '9.388', '20.954', '18.823', '7.882', '6.753', '20.895', '17.450', '20.300', '20.415', '23.101', '19.753', '18.011', '20.691', '20.992', '20.419', '22.605', '10.493', '26.598', '24.882', '24.624', '28.312', '23.993', '30.900', '25.024', '10.130', '8.032', '26.176', '26.287', '9.706', '23.908', '27.469', '26.398', '24.687', '27.235', '29.081', '33.183', '33.645', '27.564', '32.477', '36.485', '28.016', '30.558', '27.886', '27.558', '30.663', '31.294', '13.297', '30.768', '32.152', '31.705', '15.110', '31.956', '35.963', '35.194', '13.326', '32.912']
# r300 = ['1.595', '1.312', '2.296', '1.681', '1.536', '1.465', '1.563', '1.491', '2.128', '2.584', '1.903', '1.783', '1.994', '2.543', '3.074', '6.025', '3.493', '6.063', '2.084', '3.500', '2.018', '3.801', '5.541', '9.301', '4.806', '4.700', '2.888', '5.615', '6.364', '8.124', '5.786', '4.340', '9.074', '6.135', '6.416', '4.922', '9.544', '8.609', '7.784', '6.352', '7.297', '7.906', '6.559', '7.000', '12.194', '10.668', '10.560', '12.008', '11.308', '11.963', '6.449', '7.267', '14.072', '10.312', '9.425', '8.975', '13.241', '5.009', '4.917', '9.173', '4.910', '4.057', '8.924', '13.328', '8.139', '10.607', '10.899', '10.368', '5.492', '9.198', '14.730', '9.997', '9.978', '12.449', '4.827', '11.002', '7.684', '4.687', '11.364', '4.559', '4.318', '5.763', '3.422', '6.328', '11.346', '8.490', '8.094', '8.318', '8.849', '8.565', '9.906', '9.247', '8.808', '9.734', '9.891', '11.109', '3.723', '10.911', '11.186', '4.094', '10.326', '10.941', '12.316', '11.400', '12.954', '10.957', '11.901', '12.099', '13.724', '12.726', 
# '15.869', '12.570', '13.917', '15.003', '13.869', '5.586', '15.540', '12.624', '4.600', '13.108', '4.683', '14.402', '14.312', '13.874', '13.908', '15.411', '6.084', '13.484', '14.450', '14.711', '23.472', '16.606', '18.239', '17.173', '8.481', '17.016', '9.288', '18.288', '26.800', '26.164', '17.576', '19.743', '20.093', '20.460', '8.226', '7.807', '22.905', '24.555', '23.556', '9.047', '24.501', '9.480', '21.742', '20.419', '21.388', '22.738', '27.908', '15.985', '9.849', '22.173', '26.280', '22.360', '11.573', '11.562', '22.666', '8.733', '27.554', '23.739', '30.066', '29.330', '13.952', '25.261', '24.045', '10.299', '24.954', '24.534', '25.013', '10.346', '30.729', '28.085', '12.308', '27.298', '27.522', '29.257', '10.871', '26.905', '26.450', '26.553', '27.923', '29.859', '31.019', '31.155', '34.765', '35.919', '40.917', '39.674', '37.017', '33.907', '39.091', '37.148', '35.577', '36.072', '15.939', '15.413', '42.542', '46.365', '36.458', '36.392', '35.910', '36.534', '14.194', '18.220', '42.140', '38.439', '22.670', '39.690', '14.937', '42.321', '39.576', '15.585', '15.063', '39.613', '38.160', '39.726', '37.500', '37.502', '39.390', '42.271', 
# '37.705', '14.100', '14.293', '37.204', '41.379', '42.370', '14.200', '39.321', '48.217', '15.809', '15.930', '39.392', '43.288', '41.746', '39.709', '39.938', '11.879', '41.462', '12.947', '37.868', '39.452', '46.084', '43.189', '13.025', '13.943', '40.261', '45.409', '41.469', '14.710', '42.925', '15.306', '47.489', '16.458', '14.380', '14.512', '41.709', '14.694', '43.838', '43.040', '14.259', '44.164', '44.747', '18.203', '51.186', '46.575', '45.007', '48.454', '46.303', '15.720', '46.066', '48.501', '51.404', '48.359', '46.736', '16.623', '50.227', '49.358', '52.974', '59.629', '50.633', '52.445', '56.416', '58.697', '56.397', '22.090', '28.724', '56.658', '55.911', '61.040', '60.019', '61.095', '31.102']

# r100 = [float(x) for x in r100]
# r200 = [float(x) for x in r200]
# r300 = [float(x) for x in r300]

# x = np.arange(301)[1:]

# figure, axis = plt.subplots(3, 1, figsize=(10, 10))

# axis[0].plot(np.arange(301)[1:], h300, 'c')
# axis[0].plot(np.arange(201)[1:], h200, 'm')
# axis[0].plot(np.arange(101)[1:], h100, 'y')
# axis[0].set_title("hypLen")
# axis[0].legend(["300", "200", "100"])

# axis[1].plot(np.arange(301)[1:], s300, 'c')
# axis[1].plot(np.arange(201)[1:], s200, 'm')
# axis[1].plot(np.arange(101)[1:], s100, 'y')
# axis[1].set_title("sampleNr")
# axis[1].legend(["300", "200", "100"])

# axis[2].plot(np.arange(301)[1:], r300, 'c')
# axis[2].plot(np.arange(201)[1:], r200, 'm')
# axis[2].plot(np.arange(101)[1:], r100, 'y')
# axis[2].set_title("runtime")
# axis[2].legend(["300", "200", "100"])
# plt.show()

# ja = {1,2}

# b = ja.union{3}

# print(b)

# ~(v0 & v11 & v20 & v23 & v28) 88
#  Implies(v28, v6)
# ~(v1 & v15 & v27 & v28 & v6)