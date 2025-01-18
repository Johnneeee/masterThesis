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
iterations = 5 #i
templateBERT = template.replace("____", "[MASK]")
intepretorBERT = Intepretor(attributes, filePaths, neutralCases, templateBERT)

templateROBERTA = template.replace("____", "<mask>")
intepretorROBERTA = Intepretor(attributes, filePaths, neutralCases, templateROBERTA)

##########
def run(writeTo, lm, intepretor, run):
    hornAlgorithm = HornAlgorithm(intepretor, V, triggerTokens, lm) #init horn algorithm
    metadata, h, i = hornAlgorithm.learn(iterations, background) # running the horn algorithm
    path = f"{writeTo}_i{i}_r{run}"
    extractHornRulesFunctions.storeMetadata(path,metadata) # store metadata
    extractHornRulesFunctions.storeHornRules(path, h, lookupTableValues) # store extracted Horn Rules
    extractHornRulesFunctions.storeHornRulesFiltered(path, h, background, lookupTableValues) # store horn rules filtered

# run("xlmRBase", "FacebookAI/xlm-roberta-base", intepretorROBERTA, 1)
# run("xlmRBase", "FacebookAI/xlm-roberta-base", intepretorROBERTA, 2)
# run("xlmRBase", "FacebookAI/xlm-roberta-base", intepretorROBERTA, 3)
# run("xlmRBase", "FacebookAI/xlm-roberta-base", intepretorROBERTA, 4)
# run("xlmRBase", "FacebookAI/xlm-roberta-base", intepretorROBERTA, 5)
# run("xlmRBase", "FacebookAI/xlm-roberta-base", intepretorROBERTA, 6)
# run("xlmRBase", "FacebookAI/xlm-roberta-base", intepretorROBERTA, 7)
# run("xlmRBase", "FacebookAI/xlm-roberta-base", intepretorROBERTA, 8)
# run("xlmRBase", "FacebookAI/xlm-roberta-base", intepretorROBERTA, 9)
# run("xlmRBase", "FacebookAI/xlm-roberta-base", intepretorROBERTA, 10)
# writeTo = "xlmRBase"
# files = [f"{writeTo}_i{iterations}_r{n}" for n in range(1,11)]
# extractHornRulesFunctions.storeTotalCount(f"{writeTo}_i{iterations}_TotalCount",files)

# run("xlmRLarge", "FacebookAI/xlm-roberta-large", intepretorROBERTA, 1)
# run("xlmRLarge", "FacebookAI/xlm-roberta-large", intepretorROBERTA, 2)
# run("xlmRLarge", "FacebookAI/xlm-roberta-large", intepretorROBERTA, 3)
# run("xlmRLarge", "FacebookAI/xlm-roberta-large", intepretorROBERTA, 4)
# run("xlmRLarge", "FacebookAI/xlm-roberta-large", intepretorROBERTA, 5)
# run("xlmRLarge", "FacebookAI/xlm-roberta-large", intepretorROBERTA, 6)
# run("xlmRLarge", "FacebookAI/xlm-roberta-large", intepretorROBERTA, 7)
# run("xlmRLarge", "FacebookAI/xlm-roberta-large", intepretorROBERTA, 8)
# run("xlmRLarge", "FacebookAI/xlm-roberta-large", intepretorROBERTA, 9)
# run("xlmRLarge", "FacebookAI/xlm-roberta-large", intepretorROBERTA, 10)
# writeTo = "xlmRLarge"
# files = [f"{writeTo}_i{iterations}_r{n}" for n in range(1,11)]
# extractHornRulesFunctions.storeTotalCount(f"{writeTo}_i{iterations}_TotalCount",files)

run("mBertUncased", "google-bert/bert-base-multilingual-uncased", intepretorBERT, 1)
run("mBertUncased", "google-bert/bert-base-multilingual-uncased", intepretorBERT, 2)
run("mBertUncased", "google-bert/bert-base-multilingual-uncased", intepretorBERT, 3)
# run("mBertUncased", "google-bert/bert-base-multilingual-uncased", intepretorBERT, 4)
# run("mBertUncased", "google-bert/bert-base-multilingual-uncased", intepretorBERT, 5)
# run("mBertUncased", "google-bert/bert-base-multilingual-uncased", intepretorBERT, 6)
# run("mBertUncased", "google-bert/bert-base-multilingual-uncased", intepretorBERT, 7)
# run("mBertUncased", "google-bert/bert-base-multilingual-uncased", intepretorBERT, 8)
# run("mBertUncased", "google-bert/bert-base-multilingual-uncased", intepretorBERT, 9)
# run("mBertUncased", "google-bert/bert-base-multilingual-uncased", intepretorBERT, 10)
writeTo = "mBertUncased"
files = [f"{writeTo}_i{iterations}_r{n}" for n in range(1,4)]
extractHornRulesFunctions.storeTotalCount(f"{writeTo}_i{iterations}_TotalCount",files)

# run("mBertCased", "google-bert/bert-base-multilingual-cased", intepretorBERT, 1)
# run("mBertCased", "google-bert/bert-base-multilingual-cased", intepretorBERT, 2)
# run("mBertCased", "google-bert/bert-base-multilingual-cased", intepretorBERT, 3)
# run("mBertCased", "google-bert/bert-base-multilingual-cased", intepretorBERT, 4)
# run("mBertCased", "google-bert/bert-base-multilingual-cased", intepretorBERT, 5)
# run("mBertCased", "google-bert/bert-base-multilingual-cased", intepretorBERT, 6)
# run("mBertCased", "google-bert/bert-base-multilingual-cased", intepretorBERT, 7)
# run("mBertCased", "google-bert/bert-base-multilingual-cased", intepretorBERT, 8)
# run("mBertCased", "google-bert/bert-base-multilingual-cased", intepretorBERT, 9)
# run("mBertCased", "google-bert/bert-base-multilingual-cased", intepretorBERT, 10)
# writeTo = "mBertCased"
# files = [f"{writeTo}_i{iterations}_r{n}" for n in range(1,11)]
# extractHornRulesFunctions.storeTotalCount(f"{writeTo}_i{iterations}_TotalCount",files)

# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, 1)
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, 2)
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, 3)
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, 4)
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, 5)
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, 6)
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, 7)
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, 8)
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, 9)
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, 10)
# writeTo = "nbBertBase"
# files = [f"{writeTo}_i{iterations}_r{n}" for n in range(1,11)]
# extractHornRulesFunctions.storeTotalCount(f"{writeTo}_i{iterations}_TotalCount",files)


# run("nbBertLarge", "NbAiLab/nb-bert-large", intepretorBERT, 1)
# run("nbBertLarge", "NbAiLab/nb-bert-large", intepretorBERT, 2)
# run("nbBertLarge", "NbAiLab/nb-bert-large", intepretorBERT, 3)
# run("nbBertLarge", "NbAiLab/nb-bert-large", intepretorBERT, 4)
# run("nbBertLarge", "NbAiLab/nb-bert-large", intepretorBERT, 5)
# run("nbBertLarge", "NbAiLab/nb-bert-large", intepretorBERT, 6)
# run("nbBertLarge", "NbAiLab/nb-bert-large", intepretorBERT, 7)
# run("nbBertLarge", "NbAiLab/nb-bert-large", intepretorBERT, 8)
# run("nbBertLarge", "NbAiLab/nb-bert-large", intepretorBERT, 9)
# run("nbBertLarge", "NbAiLab/nb-bert-large", intepretorBERT, 10)
# writeTo = "nbBertLarge"
# files = [f"{writeTo}_i{iterations}_r{n}" for n in range(1,11)]
# extractHornRulesFunctions.storeTotalCount(f"{writeTo}_i{iterations}_TotalCount",files)

# run("norbert", "ltg/norbert", intepretorBERT, 1)
# run("norbert", "ltg/norbert", intepretorBERT, 2)
# run("norbert", "ltg/norbert", intepretorBERT, 3)
# run("norbert", "ltg/norbert", intepretorBERT, 4)
# run("norbert", "ltg/norbert", intepretorBERT, 5)
# run("norbert", "ltg/norbert", intepretorBERT, 6)
# run("norbert", "ltg/norbert", intepretorBERT, 7)
# run("norbert", "ltg/norbert", intepretorBERT, 8)
# run("norbert", "ltg/norbert", intepretorBERT, 9)
# run("norbert", "ltg/norbert", intepretorBERT, 10)
# writeTo = "norbert"
# files = [f"{writeTo}_i{iterations}_r{n}" for n in range(1,11)]
# extractHornRulesFunctions.storeTotalCount(f"{writeTo}_i{iterations}_TotalCount",files)

# run("norbert2", "ltg/norbert2", intepretorBERT, 1)
# run("norbert2", "ltg/norbert2", intepretorBERT, 2)
# run("norbert2", "ltg/norbert2", intepretorBERT, 3)
# run("norbert2", "ltg/norbert2", intepretorBERT, 4)
# run("norbert2", "ltg/norbert2", intepretorBERT, 5)
# run("norbert2", "ltg/norbert2", intepretorBERT, 6)
# run("norbert2", "ltg/norbert2", intepretorBERT, 7)
# run("norbert2", "ltg/norbert2", intepretorBERT, 8)
# run("norbert2", "ltg/norbert2", intepretorBERT, 9)
# run("norbert2", "ltg/norbert2", intepretorBERT, 10)
# writeTo = "norbert2"
# files = [f"{writeTo}_i{iterations}_r{n}" for n in range(1,11)]
# extractHornRulesFunctions.storeTotalCount(f"{writeTo}_i{iterations}_TotalCount",files)