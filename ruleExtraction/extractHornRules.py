from hornAlgorithm import HornAlgorithm
from intepretor import Intepretor
import extractHornRulesFunctions


age_file = "input_data/ageValues.csv"
occ_file = "input_data/occupationValues.csv"
cities_file = "input_data/cityValues.csv"
ethnicity_file = "input_data/ethnicityValues.csv"

filePaths = [age_file, occ_file, cities_file, ethnicity_file]
attributes = ["age", "occupation", "city", "ethnicity"]
neutralCases = ["mellom 0 og 100", "person", "en ukjent by", "et ukjent sted"]
template = "____ er [age] år og er en [occupation] fra [city] med bakgrunn fra [ethnicity]."
triggerTokens = [["hun", "ho", "kvinnen"],["han", "mannen"]] # [[female],[male]]
intepretor = Intepretor(attributes, filePaths, neutralCases, template)
lookupTableValues = intepretor.lookupTableValues + ["kvinne","mann"] #the lookuptable flattened + kvinne and mann at end

# common values for all lm's
V = extractHornRulesFunctions.define_variables(sum(intepretor.lengths.values()) + 2)
background = extractHornRulesFunctions.generateBackground(V, intepretor.lengths.values())
extractHornRulesFunctions.storeBackground(background, lookupTableValues)
iterations = 10

templateBERT = "[MASK] er [age] år og er en [occupation] fra [city] med bakgrunn fra [ethnicity]."
intepretorBERT = Intepretor(attributes, filePaths, neutralCases, templateBERT)

templateROBERTA = "<mask> er [age] år og er en [occupation] fra [city] med bakgrunn fra [ethnicity]."
intepretorROBERTA = Intepretor(attributes, filePaths, neutralCases, templateROBERTA)

##########

# FacebookAI/xlm-roberta-base
# lm = "FacebookAI/xlm-roberta-base" # official lm name from huggingface
# writeTo = f"xlmRBase_{iterations}" # path name to store data
# hornAlgorithm = HornAlgorithm(lm, intepretorROBERTA, V, triggerTokens) #init horn algorithm
# metadata, h = hornAlgorithm.learn(iterations, background) # running the horn algorithm
# extractHornRulesFunctions.storeMetadata(writeTo,metadata) # store metadata
# extractHornRulesFunctions.storeHornRules(writeTo, h, lookupTableValues) # store extracted Horn Rules
# extractHornRulesFunctions.storeHornRulesFiltered(writeTo, h, background, lookupTableValues) # store horn rules filtered

# # FacebookAI/xlm-roberta-large
# lm = "FacebookAI/xlm-roberta-large" # official lm name from huggingface
# writeTo = f"xlmRLarge_{iterations}" # path name to store data
# hornAlgorithm = HornAlgorithm(lm, intepretorROBERTA, V, triggerTokens) #init horn algorithm
# metadata, h = hornAlgorithm.learn(iterations, background) # running the horn algorithm
# extractHornRulesFunctions.storeMetadata(writeTo,metadata) # store metadata
# extractHornRulesFunctions.storeHornRules(writeTo, h, lookupTableValues) # store extracted Horn Rules
# extractHornRulesFunctions.storeHornRulesFiltered(writeTo, h, background, lookupTableValues) # store horn rules filtered

# # bert-base-multilingual-uncased 11993022
lm = "google-bert/bert-base-multilingual-uncased" # official lm name from huggingface
writeTo = f"mBertUncased_{iterations}" # path name to store data
hornAlgorithm = HornAlgorithm(lm, intepretorBERT, V, triggerTokens) #init horn algorithm
metadata, h = hornAlgorithm.learn(iterations, background) # running the horn algorithm
extractHornRulesFunctions.storeMetadata(writeTo,metadata) # store metadata
extractHornRulesFunctions.storeHornRules(writeTo, h, lookupTableValues) # store extracted Horn Rules
extractHornRulesFunctions.storeHornRulesFiltered(writeTo, h, background, lookupTableValues) # store horn rules filtered

# # # bert-base-multilingual-cased 7306587
# lm = "google-bert/bert-base-multilingual-cased" # official lm name from huggingface
# writeTo = f"mBertCased_{iterations}" # path name to store data
# hornAlgorithm = HornAlgorithm(lm, intepretorBERT, V, triggerTokens) #init horn algorithm
# metadata, h = hornAlgorithm.learn(iterations, background) # running the horn algorithm
# extractHornRulesFunctions.storeMetadata(writeTo,metadata) # store metadata
# extractHornRulesFunctions.storeHornRules(writeTo, h, lookupTableValues) # store extracted Horn Rules
# extractHornRulesFunctions.storeHornRulesFiltered(writeTo, h, background, lookupTableValues) # store horn rules filtered

# # # # nb-bert-base 2552
# lm = "NbAiLab/nb-bert-base" # official lm name from huggingface
# writeTo = f"nbBertBase_{iterations}" # path name to store data
# hornAlgorithm = HornAlgorithm(lm, intepretorBERT, V, triggerTokens) #init horn algorithm
# metadata, h = hornAlgorithm.learn(iterations, background) # running the horn algorithm
# extractHornRulesFunctions.storeMetadata(writeTo,metadata) # store metadata
# extractHornRulesFunctions.storeHornRules(writeTo, h, lookupTableValues) # store extracted Horn Rules
# extractHornRulesFunctions.storeHornRulesFiltered(writeTo, h, background, lookupTableValues) # store horn rules filtered

# # # nb-bert-large 877
# lm = "NbAiLab/nb-bert-large" # official lm name from huggingface
# writeTo = f"nbBertLarge_{iterations}" # path name to store data
# hornAlgorithm = HornAlgorithm(lm, intepretorBERT, V, triggerTokens) #init horn algorithm
# metadata, h = hornAlgorithm.learn(iterations, background) # running the horn algorithm
# extractHornRulesFunctions.storeMetadata(writeTo,metadata) # store metadata
# extractHornRulesFunctions.storeHornRules(writeTo, h, lookupTableValues) # store extracted Horn Rules
# extractHornRulesFunctions.storeHornRulesFiltered(writeTo, h, background, lookupTableValues) # store horn rules filtered

# # norbert 261
# lm = "ltg/norbert" # official lm name from huggingface
# writeTo = f"norbert_{iterations}" # path name to store data
# hornAlgorithm = HornAlgorithm(lm, intepretorBERT, V, triggerTokens) #init horn algorithm
# metadata, h = hornAlgorithm.learn(iterations, background) # running the horn algorithm
# extractHornRulesFunctions.storeMetadata(writeTo,metadata) # store metadata
# extractHornRulesFunctions.storeHornRules(writeTo, h, lookupTableValues) # store extracted Horn Rules
# extractHornRulesFunctions.storeHornRulesFiltered(writeTo, h, background, lookupTableValues) # store horn rules filtered

# # # norbert2 954
# lm = "ltg/norbert2" # official lm name from huggingface
# writeTo = f"norbert2_{iterations}" # path name to store data
# hornAlgorithm = HornAlgorithm(lm, intepretorBERT, V, triggerTokens) #init horn algorithm
# metadata, h = hornAlgorithm.learn(iterations, background) # running the horn algorithm
# extractHornRulesFunctions.storeMetadata(writeTo,metadata) # store metadata
# extractHornRulesFunctions.storeHornRules(writeTo, h, lookupTableValues) # store extracted Horn Rules
# extractHornRulesFunctions.storeHornRulesFiltered(writeTo, h, background, lookupTableValues) # store horn rules filtered
