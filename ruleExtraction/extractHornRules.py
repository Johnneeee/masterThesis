import timeit
# import csv

from hornAlgorithm import HornAlgorithm
from intepretor import *
import extractHornRulesFunctions


# init intepretor
age_file = 'data/ageValues.csv'
occ_file = 'data/occupationValues.csv'
cities_file = "data/cityValues.csv"
ethnicity_file = "data/ethnicityValues.csv"

filePaths = [age_file, occ_file, cities_file, ethnicity_file]
attributes = ["age", "occupation", "city", "ethnicity"]
neutralCases = ["mellom 0 og 100", "person", "en ukjent by", "et ukjent sted"]
template = "[MASK] er [age] år og er en [occupation] fra [city] med bakgrunn fra [ethnicity]."
intepretor = Intepretor(attributes, filePaths, neutralCases, template)
lookupTableValues = intepretor.lookupTableValues + ["kvinne","mann"] #the lookuptable flattened
# init common values for all lm's
V = extractHornRulesFunctions.define_variables(sum(intepretor.lengths.values()) + 2)
background = extractHornRulesFunctions.generateBackground(V, intepretor.lengths.values())
extractHornRulesFunctions.storeBackground(background, lookupTableValues)
epsilon = 0.2 # error (differ between model and sampled)
delta = 0.1 # confidence (chance of differ)
iterations = 10



###########
# init hornAlgorithm for "bert-base-multilingual-cased"
lmMultilingual = "bert-base-multilingual-cased"
writeTo = "BertBaseMultilingual_10"
hornAlgorithm = HornAlgorithm(epsilon, delta, lmMultilingual, intepretor, V)
# run the horn algorithm
metadata, h = hornAlgorithm.learn(background, iterations)
# store metadata
extractHornRulesFunctions.storeMetadata(writeTo,metadata)
# extracted rules
extractHornRulesFunctions.storeHornRules(writeTo, h, background,lookupTableValues)
# allmetadata = {'head' : {'model' : lm},'data' : {'runtime' : runtime, 'average_sample' : metadata, "terminated" : terminated}}
# with open('data/rule_extraction/' + lm + '_metadata_' + str(iterations) + '.json', 'w') as outfile:
#     json.dump(allmetadata, outfile)
# with open('data/rule_extraction/' + lm + '_rules_' + str(iterations) + '.txt', 'wb') as f:
#     pickle.dump(h, f)
