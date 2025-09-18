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
print(sum(ja)/len(ja))
# print([d[x] for x in hele])