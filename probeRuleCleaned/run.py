from hornAlgorithm import HornAlgorithm
from intepretor import Intepretor
import runFunctions

# getting input filenames
age_file = "input_data/ageValues.csv"
occ_file = "input_data/occupationValues.csv"
livingLoc_file = "input_data/livingLocValues.csv"
ethnicity_file = "input_data/ethnicityValues.csv"
gender_file = "input_data/genderValues.csv"

# init sentence template and its variables
template = "____ er [AGES] år og er en [OCCUPATIONS] fra [LIVINGLOCATIONS] med bakgrunn fra [ETHNICITIES]." # placeholders has to match the header in the input files
filePaths = [age_file, occ_file, livingLoc_file, ethnicity_file, gender_file]

# defining catch cases for each gender
catchCases = [["hun", "ho", "henne", "kvinnen"], ["han", "mannen"]] # [[female],[male]]

# init two intepretor variants
intepretorBERT = Intepretor(filePaths, template.replace("____", "[MASK]")) # BERT models uses [MASK]
# intepretorROBERTA = Intepretor(attributes, filePaths, neutralCases, template.replace("____", "<mask>")) # RoBERTa models uses <mask>

# getting the lookuptable 
lookupTable = intepretorBERT.lookupTable # intepretorBERT and intepretorROBERT has the same lookuptable 

# init vocabulary and background
V = runFunctions.define_variables(sum(intepretorBERT.lengths.values()))
background = runFunctions.generateBackground(V, intepretorBERT.lengths.values())
runFunctions.storeBackground(background, lookupTable)

##########
def run(writeTo, lm, intepretor, run, iterations):
    """
        writeTo     : the output filename
        lm          : language model name from huggingface
        intepretor  : either intepretorBERT or intepretorROBERT: intepretorBERT uses [MASK], intepretorBERT uses <mask>
        run         : run number indication tagged on the output filename
        iterations  : iteration cap for the horn algorithm. This is also tagged on the output filename
    """
    hornAlgorithm = HornAlgorithm(intepretor, V, catchCases, lm) #init horn algorithm
    metadata, hornRules, iterations = hornAlgorithm.learn(iterations, background) # running the horn algorithm
    path = f"{writeTo}_i{iterations}_r{run}" # making the file name
    runFunctions.storeMetadata(path,metadata) # store metadata
    runFunctions.storeHornRules(path, hornRules, lookupTable) # store horn rules


run("test", "ltg/norbert", intepretorBERT, run=0, iterations=10) #test

# e.g.
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, run=0, iterations=100)
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, run=1, iterations=100)
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, run=2, iterations=100)
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, run=0, iterations=200)
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, run=1, iterations=200)
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, run=0, iterations=300)
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, run=1, iterations=300)
# run("nbBertBase", "NbAiLab/nb-bert-base", intepretorBERT, run=2, iterations=300)
