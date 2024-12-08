import numpy as np
import timeit
from itertools import combinations
from hornAlgorithm import *
from intepretor import *


def define_variables(number):
    s = "".join(['v'+str(i)+',' for i in range(number)])
    V = [e for e in symbols(s)]
    return V

def generateBackground(V, attLengths):
    # two values from the same attrutube dimention cant be true simultaneously
    splitIndexes = []
    i = 0
    for x in attLengths:
        i += x
        splitIndexes.append(i)
    splitted = np.split(V, splitIndexes)
    background = set()

    for x in splitted:
        background.update(set(combinations(x, 2)))

    background = set(map(lambda x: ~(x[0] & x[1]),background))
    return background


# init intepretor
age_file = 'data/ageValues.csv'
occ_file = 'data/occupationValues.csv'
cities_file = "data/cityValues.csv"
ethnicity_file = "data/ethnicityValues.csv"

filePaths = [age_file, occ_file, cities_file, ethnicity_file]
attributes = ["age", "occupation", "city", "ethnicity"]
neutralCases = ["mellom 0 og 100", "person", "en ukjent by", "et ukjent sted"]
template = "<mask> er [age] år og er en [occupation] fra [city] med bakgrunn fra [ethnicity]."
intepretor = Intepretor(attributes, filePaths, neutralCases, template)


# init hornAlgorithm for "bert-base-multilingual-cased"
V = define_variables(sum(intepretor.lengths.values()) + 2)

lm = "bert-base-multilingual-cased"
epsilon = 0.2
delta = 0.1
hornAlgorithm = HornAlgorithm(epsilon, delta, lm, intepretor, V)

# run the horn algorithm
# background = generateBackground(V, intepretor.lengths.values()) 
background = {}
iterations = 30

start = timeit.default_timer()
terminated, metadata, h = hornAlgorithm.learn(background, iterations)
stop = timeit.default_timer()
runtime = stop-start

# for lm in LMs:
#     (h,runtime,terminated,average_samples) = extractHornRules(attributes, lm, V, iterations, intepretor, background)
#     metadata = {'head' : {'model' : lm, 'experiment' : r+1},'data' : {'runtime' : runtime, 'average_sample' : average_samples, "terminated" : terminated}}
#     with open('data/rule_extraction/' + lm + '_metadata_' + str(iterations) + "_" + str(r+1) + '.json', 'w') as outfile:
#         json.dump(metadata, outfile)
#     with open('data/rule_extraction/' + lm + '_rules_' + str(iterations) + "_" + str(r+1) + '.txt', 'wb') as f:
#         pickle.dump(h, f)
