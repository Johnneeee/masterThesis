import numpy as np
import random
import timeit
from transformers import pipeline
# from helper_functions import *
from scipy.special import comb
import pickle
import json
# from re_eval_methods import *

from hornAlgorithm import *
from intepretor import *


def define_variables(number):
    s = "".join(['v'+str(i)+',' for i in range(number)])
    V = [e for e in symbols(s)]
    return V

def generateBackground(V): # just a random background pattern generator
    background = set()
    for i in range(len(V)-3):
        for j in range(3):
            background.add(~(V[i] & V[i+j]))
    return background

def extractHornRules(template,attributes, lm, V, iterations, intepretor, background):
    bad_pc = []
    bad_ne =[]
    unmasker = pipeline('fill-mask', model=lm)
    mq = lambda a : custom_MQ(template, a, lm, unmasker, intepretor)
    eq = lambda a : custom_EQ(template, attributes, a, lm, unmasker, V, bad_ne, intepretor)
    start = timeit.default_timer()
    terminated, metadata, h = hornAlgorithm(V, mq, eq, bad_ne, bad_pc, background, iterations)
    stop = timeit.default_timer()
    runtime = stop-start

    return (h,runtime, terminated, metadata)

# init intepretor
age_file = 'data/ageValues.csv'
occ_file = 'data/occupationValues.csv'
cities_file = "data/cityValues.csv"
ethnicity_file = "data/ethnicityValues.csv"

filePaths = [age_file, occ_file, cities_file, ethnicity_file]
attributes = ['age', 'occupation', "city", "ethnicity"]
neutralCases = ["mellom 0 og 100", "person", "en ukjent by", "et ukjent sted"]
template = "<mask> er [age] år og er en [occupation] fra [city] med bakgrunn fra [ethnicity]."
intepretor = Intepretor(attributes, filePaths, neutralCases, template)



nValues = sum(intepretor.lengths.values()) + 2
V = define_variables(nValues)
LMs = ['bert-base-multilingual-cased'] #more models 4/5? all occs
# language_model = models[0]

# epsilon = 0.2
# delta = 0.1

background = generateBackground(V)

iterations = 30
# # eq = 5000
r=0
for lm in LMs:
    (h,runtime,terminated,average_samples) = extractHornRules(template, attributes, lm, V, iterations, intepretor, background)
    metadata = {'head' : {'model' : lm, 'experiment' : r+1},'data' : {'runtime' : runtime, 'average_sample' : average_samples, "terminated" : terminated}}
    with open('data/rule_extraction/' + lm + '_metadata_' + str(iterations) + "_" + str(r+1) + '.json', 'w') as outfile:
        json.dump(metadata, outfile)
    with open('data/rule_extraction/' + lm + '_rules_' + str(iterations) + "_" + str(r+1) + '.txt', 'wb') as f:
        pickle.dump(h, f)
