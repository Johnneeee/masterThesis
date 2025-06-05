from hornAlgorithm import HornAlgorithm
from intepretor import Intepretor
import runFunctions

# getting input filenames
age_file = "input_data/ageValues.csv"
occ_file = "input_data/occupationValues.csv"
livingLoc_file = "input_data/livingLocValues.csv"
ethnicity_file = "input_data/ethnicityValues.csv"

# init variables
filePaths = [age_file, occ_file, livingLoc_file, ethnicity_file]
attributes = ["age", "occupation", "livingLoc", "ethnicity"]
neutralCases = ["mellom 0 og 100", "person", "en ukjent by", "et ukjent sted"]

template = "____ er [age] år og er en [occupation] fra [livingLoc] med bakgrunn fra [ethnicity]."
triggerTokens = [["hun", "ho", "henne", "kvinnen"],["han", "mannen"]] # [[female],[male]]
intepretor = Intepretor(attributes, filePaths, neutralCases, template)
lookupTableValues = intepretor.lookupTableValues + ["kvinne","mann"] #the lookuptable flattened + kvinne and mann at end

# common values for all lm's
V = runFunctions.define_variables(sum(intepretor.lengths.values()) + 2)
background = runFunctions.generateBackground(V, intepretor.lengths.values())
runFunctions.storeBackground(background, lookupTableValues)

# init two intepretor variants
intepretorBERT = Intepretor(attributes, filePaths, neutralCases, template.replace("____", "[MASK]")) # BERT models uses [MASK]
intepretorROBERTA = Intepretor(attributes, filePaths, neutralCases, template.replace("____", "<mask>")) # RoBERTa models uses <mask>

##########
def run(writeTo, lm, intepretor, run, iterations):
    """
        writeTo     : the output filename
        lm          : language model name from huggingface
        intepretor  : either intepretorBERT or intepretorROBERT: intepretorBERT uses [MASK], intepretorBERT uses <mask>
        run         : run number indication tagged on the output filename
        iterations  : iteration cap for the horn algorithm. This is also tagged on the output filename
    """
    hornAlgorithm = HornAlgorithm(intepretor, V, triggerTokens, lm) #init horn algorithm
    metadata, h, i = hornAlgorithm.learn(iterations, background) # running the horn algorithm
    path = f"{writeTo}_i{i}_r{run}" # making the file name
    runFunctions.storeMetadata(path,metadata) # store metadata
    runFunctions.storeHornRules(path, h, lookupTableValues) # store horn rules


# run("test", "ltg/norbert", intepretorBERT, run=0, iterations=10) #test

# e.g.
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, run=0, iterations=100)
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, run=1, iterations=100)
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, run=2, iterations=100)
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, run=0, iterations=200)
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, run=1, iterations=200)
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, run=0, iterations=300)
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, run=1, iterations=300)
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, run=2, iterations=300)
