from hornAlgorithm import HornAlgorithm
from intepretor import Intepretor
import extractHornRulesFunctions


age_file = "input_data/ageValues.csv"
occ_file = "input_data/occupationValues.csv"
cities_file = "input_data/cityValues.csv"
ethnicity_file = "input_data/ethnicityValues.csv"

filePaths = [age_file, occ_file, cities_file, ethnicity_file]
attributes = ["age", "occupation", "city", "ethnicity"]
neutralCases = ["mellom 0 og 100", " en person", "en ukjent by", "et ukjent sted"]
template = "____ er [age] år og er en [occupation] fra [city] med bakgrunn fra [ethnicity]."
triggerTokens = [["hun", "ho", "kvinnen"],["han", "mannen"]] # [[female],[male]]
intepretor = Intepretor(attributes, filePaths, neutralCases, template)
lookupTableValues = intepretor.lookupTableValues + ["kvinne","mann"] #the lookuptable flattened + kvinne and mann at end

# common values for all lm's
V = extractHornRulesFunctions.define_variables(sum(intepretor.lengths.values()) + 2)
background = extractHornRulesFunctions.generateBackground(V, intepretor.lengths.values())
extractHornRulesFunctions.storeBackground(background, lookupTableValues)
iterations = 10 #i
loop = 5 #r
templateBERT = template.replace("____", "[MASK]")
intepretorBERT = Intepretor(attributes, filePaths, neutralCases, templateBERT)

templateROBERTA = template.replace("____", "<mask>")
intepretorROBERTA = Intepretor(attributes, filePaths, neutralCases, templateROBERTA)

##########

# "[MASK] er [age] år og er en [occupation] fra [city] med bakgrunn fra [ethnicity]."

# "[MASK] er mellom 20 og 30 år og er lege i Bergen med bakgrunn fra Afrika" 

# FacebookAI/xlm-roberta-base
# hornAlgorithm = HornAlgorithm(intepretorROBERTA, V, triggerTokens, "FacebookAI/xlm-roberta-base") #init horn algorithm
# metadata, h, i =  hornAlgorithm.learn(iterations, background) # running the horn algorithm
# writeTo = f"xlmRBase_{i}" # path name to store data
# extractHornRulesFunctions.storeMetadata(writeTo,metadata) # store metadata
# extractHornRulesFunctions.storeHornRules(writeTo, h, lookupTableValues) # store extracted Horn Rules
# extractHornRulesFunctions.storeHornRulesFiltered(writeTo, h, background, lookupTableValues) # store horn rules filtered

# # FacebookAI/xlm-roberta-large
# hornAlgorithm = HornAlgorithm(intepretorROBERTA, V, triggerTokens, "FacebookAI/xlm-roberta-large") #init horn algorithm
# metadata, h, i =  hornAlgorithm.learn(iterations, background) # running the horn algorithm
# writeTo = f"xlmRLarge_{i}" # path name to store data
# extractHornRulesFunctions.storeMetadata(writeTo,metadata) # store metadata
# extractHornRulesFunctions.storeHornRules(writeTo, h, lookupTableValues) # store extracted Horn Rules
# extractHornRulesFunctions.storeHornRulesFiltered(writeTo, h, background, lookupTableValues) # store horn rules filtered

# # bert-base-multilingual-uncased 11993022
writeTo = "mBertUncased"
for r in range(1,loop+1):
    hornAlgorithm = HornAlgorithm(intepretorBERT, V, triggerTokens, "google-bert/bert-base-multilingual-uncased") #init horn algorithm
    metadata, h, i = hornAlgorithm.learn(iterations, background) # running the horn algorithm
    # writeTo = f"mBertUncased_i{i}_r{n}" # path name to store data
    extractHornRulesFunctions.storeMetadata(f"{writeTo}_i{i}_r{r}",metadata) # store metadata
    extractHornRulesFunctions.storeHornRules(f"{writeTo}_i{i}_r{r}", h, lookupTableValues) # store extracted Horn Rules
    extractHornRulesFunctions.storeHornRulesFiltered(writeTo, h, background, lookupTableValues) # store horn rules filtered
files = [f"mBertUncased_i{iterations}_r{n}" for n in range(1,loop+1)]
extractHornRulesFunctions.storeTotalCount(f"{writeTo}_i{iterations}TotalCount",files, background)

# # # bert-base-multilingual-cased 7306587
# hornAlgorithm = HornAlgorithm(intepretorBERT, V, triggerTokens, "google-bert/bert-base-multilingual-cased") #init horn algorithm
# metadata, h, i =  hornAlgorithm.learn(iterations, background) # running the horn algorithm
# writeTo = f"mBertCased_{i}" # path name to store data
# extractHornRulesFunctions.storeMetadata(writeTo,metadata) # store metadata
# extractHornRulesFunctions.storeHornRules(writeTo, h, lookupTableValues) # store extracted Horn Rules
# extractHornRulesFunctions.storeHornRulesFiltered(writeTo, h, background, lookupTableValues) # store horn rules filtered

# # # # nb-bert-base 2552
# hornAlgorithm = HornAlgorithm(intepretorBERT, V, triggerTokens, "NbAiLab/nb-bert-base") #init horn algorithm
# metadata, h, i =  hornAlgorithm.learn(iterations, background) # running the horn algorithm
# writeTo = f"nbBertBase_{i}" # path name to store data
# extractHornRulesFunctions.storeMetadata(writeTo,metadata) # store metadata
# extractHornRulesFunctions.storeHornRules(writeTo, h, lookupTableValues) # store extracted Horn Rules
# extractHornRulesFunctions.storeHornRulesFiltered(writeTo, h, background, lookupTableValues) # store horn rules filtered

# # # nb-bert-large 877
# hornAlgorithm = HornAlgorithm(intepretorBERT, V, triggerTokens, "NbAiLab/nb-bert-large") #init horn algorithm
# metadata, h, i =  hornAlgorithm.learn(iterations, background) # running the horn algorithm
# writeTo = f"nbBertLarge_{i}" # path name to store data
# extractHornRulesFunctions.storeMetadata(writeTo,metadata) # store metadata
# extractHornRulesFunctions.storeHornRules(writeTo, h, lookupTableValues) # store extracted Horn Rules
# extractHornRulesFunctions.storeHornRulesFiltered(writeTo, h, background, lookupTableValues) # store horn rules filtered

# # norbert 261
# hornAlgorithm = HornAlgorithm(intepretorBERT, V, triggerTokens, "ltg/norbert") #init horn algorithm
# metadata, h, i =  hornAlgorithm.learn(iterations, background) # running the horn algorithm
# writeTo = f"norbert_{i}" # path name to store data
# extractHornRulesFunctions.storeMetadata(writeTo,metadata) # store metadata
# extractHornRulesFunctions.storeHornRules(writeTo, h, lookupTableValues) # store extracted Horn Rules
# extractHornRulesFunctions.storeHornRulesFiltered(writeTo, h, background, lookupTableValues) # store horn rules filtered

# # # norbert2 954
# hornAlgorithm = HornAlgorithm(intepretorBERT, V, triggerTokens, "ltg/norbert2") #init horn algorithm
# metadata, h, i =  hornAlgorithm.learn(iterations, background) # running the horn algorithm
# writeTo = f"norbert2_{i}" # path name to store data
# extractHornRulesFunctions.storeMetadata(writeTo,metadata) # store metadata
# extractHornRulesFunctions.storeHornRules(writeTo, h, lookupTableValues) # store extracted Horn Rules
# extractHornRulesFunctions.storeHornRulesFiltered(writeTo, h, background, lookupTableValues) # store horn rules filtered
