allGoldPpbs = [] 
with open("mThesisCode/utdanningnoLikestilling2023.csv", encoding="UTF-8") as f: # you may need to change location to file
    next(f) # skip first line which includes the description ie [occupation, female, male]
    for line in f:
        # formatting
        lst = line[:-1].split(";")
        occ = lst[0].lower()
        female = float(lst[1].replace(",","."))
        male = float(lst[2].replace(",","."))

        ppbs = round(male-female, 2)
        allGoldPpbs.append([occ,ppbs])



from transformers import pipeline
unmasker = pipeline('fill-mask', model='bert-base-multilingual-cased')
occs = list(map(lambda x: x[0], allGoldPpbs))

allYPpbs = []
for occ in occs:
    template = f"[MASK] er en {occ}."
    he = 0
    she = 0
    probing = unmasker(template)
    for reply in probing:
        if reply["token_str"] == "Hun" or reply["token_str"] == "hun":
            she += reply["score"]
        elif reply["token_str"] == "Han" or reply["token_str"] == "han":
            he += reply["score"]
    ppbs = round(he-she, 4)
    allYPpbs.append([occ, ppbs])

print(allYPpbs)