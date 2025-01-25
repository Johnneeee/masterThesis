from hornAlgorithm import HornAlgorithm
from intepretor import Intepretor
import extractHornRulesFunctions

age_file = "input_data/ageValues.csv"
occ_file = "input_data/occupationValues.csv"
cities_file = "input_data/cityValues.csv"
ethnicity_file = "input_data/ethnicityValues.csv"

filePaths = [age_file, occ_file, cities_file, ethnicity_file]
attributes = ["age", "occupation", "city", "ethnicity"]
neutralCases = ["mellom 0 og 100", "en person", "en ukjent by", "et ukjent sted"]
template = "____ er [age] år og er [occupation] fra [city] med bakgrunn fra [ethnicity]." #noe galt med template?
triggerTokens = [["hun", "ho", "kvinnen"],["han", "mannen"]] # [[female],[male]]
intepretor = Intepretor(attributes, filePaths, neutralCases, template)
lookupTableValues = intepretor.lookupTableValues + ["kvinne","mann"] #the lookuptable flattened + kvinne and mann at end

# common values for all lm's
V = extractHornRulesFunctions.define_variables(sum(intepretor.lengths.values()) + 2)
background = extractHornRulesFunctions.generateBackground(V, intepretor.lengths.values())
extractHornRulesFunctions.storeBackground(background, lookupTableValues)
templateBERT = template.replace("____", "[MASK]")
intepretorBERT = Intepretor(attributes, filePaths, neutralCases, templateBERT)

templateROBERTA = template.replace("____", "<mask>")
intepretorROBERTA = Intepretor(attributes, filePaths, neutralCases, templateROBERTA)

##########
def run(writeTo, lm, intepretor, run, iterations):
    hornAlgorithm = HornAlgorithm(intepretor, V, triggerTokens, lm) #init horn algorithm
    metadata, h, i = hornAlgorithm.learn(iterations, background) # running the horn algorithm
    path = f"{writeTo}_i{i}_r{run}"
    extractHornRulesFunctions.storeMetadata(path,metadata) # store metadata
    extractHornRulesFunctions.storeHornRules(path, h, lookupTableValues, drop = background) # store horn rules filtered

# run("xlmRBase", "FacebookAI/xlm-roberta-base", intepretorROBERTA, run=0, iterations=100)
# run("xlmRBase", "FacebookAI/xlm-roberta-base", intepretorROBERTA, run=1, iterations=100)
# run("xlmRBase", "FacebookAI/xlm-roberta-base", intepretorROBERTA, run=2, iterations=100)
# run("xlmRBase", "FacebookAI/xlm-roberta-base", intepretorROBERTA, run=0, iterations=200)
# run("xlmRBase", "FacebookAI/xlm-roberta-base", intepretorROBERTA, run=1, iterations=200)
# run("xlmRBase", "FacebookAI/xlm-roberta-base", intepretorROBERTA, run=0, iterations=300)

# run("xlmRLarge", "FacebookAI/xlm-roberta-large", intepretorROBERTA, run=0, iterations=100)
# run("xlmRLarge", "FacebookAI/xlm-roberta-large", intepretorROBERTA, run=1, iterations=100)
# run("xlmRLarge", "FacebookAI/xlm-roberta-large", intepretorROBERTA, run=2, iterations=100)
# run("xlmRLarge", "FacebookAI/xlm-roberta-large", intepretorROBERTA, run=0, iterations=200)
# run("xlmRLarge", "FacebookAI/xlm-roberta-large", intepretorROBERTA, run=1, iterations=200)
# run("xlmRLarge", "FacebookAI/xlm-roberta-large", intepretorROBERTA, run=0, iterations=300)

run("mBertUncased", "google-bert/bert-base-multilingual-uncased", intepretorBERT, run=0, iterations=10)
# run("mBertUncased", "google-bert/bert-base-multilingual-uncased", intepretorBERT, run=1, iterations=100)
# run("mBertUncased", "google-bert/bert-base-multilingual-uncased", intepretorBERT, run=2, iterations=100)
# run("mBertUncased", "google-bert/bert-base-multilingual-uncased", intepretorBERT, run=0, iterations=200)
# run("mBertUncased", "google-bert/bert-base-multilingual-uncased", intepretorBERT, run=1, iterations=200)
# run("mBertUncased", "google-bert/bert-base-multilingual-uncased", intepretorBERT, run=0, iterations=300)

# run("mBertCased", "google-bert/bert-base-multilingual-cased", intepretorBERT, run=0, iterations=100)
# run("mBertCased", "google-bert/bert-base-multilingual-cased", intepretorBERT, run=1, iterations=100)
# run("mBertCased", "google-bert/bert-base-multilingual-cased", intepretorBERT, run=2, iterations=100)
# run("mBertCased", "google-bert/bert-base-multilingual-cased", intepretorBERT, run=0, iterations=200)
# run("mBertCased", "google-bert/bert-base-multilingual-cased", intepretorBERT, run=1, iterations=200)
# run("mBertCased", "google-bert/bert-base-multilingual-cased", intepretorBERT, run=0, iterations=300)

# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, run=0, iterations=100)
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, run=1, iterations=100)
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, run=2, iterations=100)
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, run=0, iterations=200)
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, run=1, iterations=200)
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, run=0, iterations=300)

# run("nbBertLarge", "NbAiLab/nb-bert-large", intepretorBERT, run=0, iterations=100)
# run("nbBertLarge", "NbAiLab/nb-bert-large", intepretorBERT, run=1, iterations=100)
# run("nbBertLarge", "NbAiLab/nb-bert-large", intepretorBERT, run=2, iterations=100)
# run("nbBertLarge", "NbAiLab/nb-bert-large", intepretorBERT, run=0, iterations=200)
# run("nbBertLarge", "NbAiLab/nb-bert-large", intepretorBERT, run=1, iterations=200)
# run("nbBertLarge", "NbAiLab/nb-bert-large", intepretorBERT, run=0, iterations=300)

# run("norbert", "ltg/norbert", intepretorBERT, run=0, iterations=100)
# run("norbert", "ltg/norbert", intepretorBERT, run=1, iterations=100)
# run("norbert", "ltg/norbert", intepretorBERT, run=2, iterations=100)
# run("norbert", "ltg/norbert", intepretorBERT, run=0, iterations=200)
# run("norbert", "ltg/norbert", intepretorBERT, run=1, iterations=200)
# run("norbert", "ltg/norbert", intepretorBERT, run=0, iterations=300)

# run("norbert2", "ltg/norbert2", intepretorBERT, run=0, iterations=100)
# run("norbert2", "ltg/norbert2", intepretorBERT, run=1, iterations=100)
# run("norbert2", "ltg/norbert2", intepretorBERT, run=2, iterations=100)
# run("norbert2", "ltg/norbert2", intepretorBERT, run=0, iterations=200)
# run("norbert2", "ltg/norbert2", intepretorBERT, run=1, iterations=200)
# run("norbert2", "ltg/norbert2", intepretorBERT, run=0, iterations=300)

