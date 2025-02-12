from transformers import pipeline
import csv
from tqdm import tqdm

def readCSV(path): # -> # [[occ,p_she,p_he,gold_ppbs]]
    data = []
    with open(path, encoding = "UTF-8") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader) # skip first line which includes the description, ie [occupation, female, male]
        data = [[x[0]] + [float(y) for y in x[1:]] for x in reader]
    return data


def probePPBS(occupations, templates, maskTag, lm):
    templates = list(map(lambda x: x.replace("____", maskTag), templates))
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
                if token in {"hun", "ho", "henne", "kvinnen"}: # add more cases?
                    she += res["score"]

                #if male
                elif token in {"han", "mannen"}: # add more cases?
                    he += res["score"]

            ppbss_occ.append(round(he-she,3))

        avg = sum(ppbss_occ) / len(ppbss_occ)
        pred_PPBSs[occ] = round(avg,3)

    return pred_PPBSs # bias: + == male, - == female


def writeCSV(path, gold_data, pred_data):
    data = list(map(lambda x: [x[0],x[3],pred_data[x[0]]],gold_data)) 
    head = [["ATTRIBUTE", "GOLD", "PRED"]]

    with open(path, 'w', newline='', encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerows(head)
        writer.writerows(data)
##########################################################################
# init data for probing

# same templates for all lm probings
# chatgpt helped with creative template ideas
templates = [
    "____ er en [OCCUPATION].",
    "____ jobber som [OCCUPATION].",
    "____ jobbet som [OCCUPATION].",
    "____ skal jobbe som [OCCUPATION].",
    "____ vil jobbe som [OCCUPATION].",
    "____ ville jobbe som [OCCUPATION].",
    "____ kommer til å jobbe som [OCCUPATION].",
    "____ begynte å jobbe som [OCCUPATION].",
    "____ har jobbet som [OCCUPATION].",
    "____ hadde jobbet som [OCCUPATION].",
    "____ kunne jobbe som [OCCUPATION].",
    "____ ønsker å jobbe som [OCCUPATION].",
    "____ pleide å jobbe som [OCCUPATION].",
    "____ fortsetter å jobbe som [OCCUPATION].",
    "____ drømmer om å jobbe som [OCCUPATION].",
    "____ skal snart jobbe som [OCCUPATION].",
    "____ fikk en jobb som [OCCUPATION].",
    "____ søkte på en jobb som [OCCUPATION].",
    "____ planlegger å jobbe som [OCCUPATION].",
    "____ kan jobbe som [OCCUPATION].",
    "____ lærte å jobbe som [OCCUPATION]."
]

# gender distribution across occupations in norway 2023. (utdanning.no)
gold_data = readCSV("../censusData/preparedData/utdanningnoLikestilling2023_ppbs.csv")
occs = list(map(lambda x: x[0],gold_data))
bert = "[MASK]"
roberta = "<mask>"

##########################################################################
# probing gender given occupation

pred_data = probePPBS(occs[:2], templates[:2], roberta, "FacebookAI/xlm-roberta-base")
writeCSV("data/raw/xlmRBaseskskks_ppbs.csv", gold_data[:2], pred_data)

pred_data = probePPBS(occs, templates, roberta, "FacebookAI/xlm-roberta-large")
writeCSV("data/raw/xlmRLarge_ppbs.csv", gold_data, pred_data)

pred_data = probePPBS(occs, templates, bert, "google-bert/bert-base-multilingual-uncased")
writeCSV("data/raw/mBertUncased_ppbs.csv", gold_data, pred_data)

pred_data = probePPBS(occs, templates, bert, "google-bert/bert-base-multilingual-cased")
writeCSV("data/raw/mBertCased_ppbs.csv", gold_data, pred_data)

pred_data = probePPBS(occs, templates, bert, "NbAiLab/nb-bert-base")
writeCSV("data/raw/nbBertBase_ppbs.csv", gold_data, pred_data)

pred_data = probePPBS(occs, templates, bert, "NbAiLab/nb-bert-large")
writeCSV("data/raw/nbBertLarge_ppbs.csv", gold_data, pred_data)

pred_data = probePPBS(occs, templates, bert, "ltg/norbert")
writeCSV("data/raw/norbert_ppbs.csv", gold_data, pred_data)

pred_data = probePPBS(occs, templates, bert, "ltg/norbert2")
writeCSV("data/raw/norbert2_ppbs.csv", gold_data, pred_data)
