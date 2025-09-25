# from transformers import pipeline
# unmasker = pipeline('fill-mask', model='ltg/norbert2')


# for x in unmasker("[MASK] er eldre enn 60 år og er en sykepleier fra en ukjent by med bakgrunn fra Australia."):
#     print(x)

d = {
    "a": 4,
    "b": 3,
    "c": 2,
    "d": 1,
}

uib = ["c","c","c","b","c","c","c","d","d","b","d","d","b","d","b","c","c"]
uio = ["d","c","d","c","b","c"]

hele = uib+uio
# print(d["a"])
ja = [d[x] for x in hele]
# print(sum(ja)/len(ja))
# print([d[x] for x in hele])

text = " 15 & 11 & 8/72 & mellom 30 og 40 \& kvinne \& advokat ---> FALSE \\ \hline"

liste = ["kvinne", "---> FALSE"]
# if token in {"hun", "ho", "henne", "kvinnen"}
# if all(n in text for n in liste) and text.count("&") == 5:
#     print(text)
# if ("1" in text) and ("2" in text) and text.count("&") == 5:
#     print(text)

a = [1,1,1,1,1,1]
b = [1,1,1,1,1,1]

ja = [a[i] + b[i] for i in range(len(a))]
print(ja)