from transformers import pipeline
import csv
from tqdm import tqdm

def readFromCSV(path):
    data = []
    with open(path, encoding = "UTF-8") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader) # skip first line which includes the description, ie [occupation, female, male]
        for line in reader:
            occ = line[0].lower()
            she = round(float(line[1])/100, 3) # /100 to turn into percentage
            he = round(float(line[2])/100, 3)
            gold_ppbs = round(he-she,3)
            data.append([occ,she,he,gold_ppbs])
        return data # [[occ,p_she,p_he,gold_ppbs]]
    
def probePPBS(occupations, templates, lm):
    unmasker = pipeline('fill-mask', model=lm) # using bert-base-multilingual-cased as model
    pred_PPBSs = {} # all occupations: {occupation: ppbs}
    for i in tqdm(range(len(occupations)), desc="Occupation"):
        occ = occupations[i]
        ppbss_occ = [] # same occupation, diff templates: [ppbs]
        for template in templates:
            setTemplate = template.replace("[OCCUPATION]", occ) #replacing [OCCUPATION] with the an occupation in the sentence
            he = 0 #init
            she = 0 # init
            results = unmasker(setTemplate) # probing

            for res in results: # for the replies returned by the language model
                token = (res["token_str"]).lower()
                #if female
                if token in {"hun", "ho", "kvinnen"}: # add more cases?
                    she += res["score"]

                #if male
                elif token in {"han", "mannen"}: # add more cases?
                    he += res["score"]

            ppbss_occ.append(round(he-she,3))

        avg = sum(ppbss_occ) / len(ppbss_occ)
        pred_PPBSs[occ] = round(avg,3)

    return pred_PPBSs # bias: + == male, - == female

def writeToCSV(path, gold_data, pred_data):
    data = list(map(lambda x: [x[0],x[3],pred_data[x[0]]],gold_data)) 
    head = [["ATTRIBUTE", "GOLD", "PRED"]]

    with open(path, 'w', newline='', encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerows(head)
        writer.writerows(data)

########################################################

gold_data = readFromCSV("../censusData/utdanningnoLikestilling2023.csv")

occs = list(map(lambda x: x[0],gold_data))
# same templates for all lm probings
templates = ["[MASK] er en [OCCUPATION].",
             "[MASK] jobber som [OCCUPATION].",
             "[MASK] jobbet som [OCCUPATION].",
             "[MASK] skal jobbe som [OCCUPATION].",
             "[MASK] vil jobbe som [OCCUPATION].",
             "[MASK] ville jobbe som [OCCUPATION].",
             "[MASK] kommer til å jobbe som [OCCUPATION].",
             "[MASK] skal jobbe som [OCCUPATION].",
             ]


pred_data = probePPBS(occs, templates, "google-bert/bert-base-multilingual-uncased")
writeToCSV("data/bbMultiUncased_ppbs.csv", gold_data, pred_data)

pred_data = probePPBS(occs, templates, "google-bert/bert-base-multilingual-cased")
writeToCSV("data/bbMultiCased_ppbs.csv", gold_data, pred_data)

pred_data = probePPBS(occs, templates, "NbAiLab/nb-bert-base")
writeToCSV("data/nbBertBase_ppbs.csv", gold_data, pred_data)

pred_data = probePPBS(occs, templates, "NbAiLab/nb-bert-large")
writeToCSV("data/nbBertLarge_ppbs.csv", gold_data, pred_data)

pred_data = probePPBS(occs, templates, "ltg/norbert")
writeToCSV("data/norbert_ppbs.csv", gold_data, pred_data)

pred_data = probePPBS(occs, templates, "ltg/norbert2")
writeToCSV("data/norbert2_ppbs.csv", gold_data, pred_data)

