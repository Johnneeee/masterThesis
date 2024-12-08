from sympy import *
import numpy as np
import random

attributes = ["age", "occupation", "city", "ethnicity"]
lengths = {"age": 6, "occupation" : 8, "city" : 8, "ethnicity" : 6}

def getRandomValue(length, allow_zero):
    vec = list(np.zeros(length, dtype=np.int8))
    # allow for all zeroes: one extra sample length and if its out of index range, use all zeroes vector (equal possibility)
    if allow_zero:
        myI = random.randrange(length)
        i = random.sample(range(length + 1), k=1)[0]
        # print(length)
        print(myI)
        # print(i)
    else:
        i = random.sample(range(length), k=1)[0]
    if i < length:
        vec[i] = 1
    return vec

# print(random.randrange(0,10))
# random.randrange(20, 50, 3)
# print(not True)

def get_label(classification, gender):
    """
        Does handling no 1 in vector work as a diverse attribute (neither he or she) to include they?
        -> never gets predicted so what rules result from that? Influences other attributes?
    """
    if (gender[0] == 1 and classification == 0) or (gender[1] == 1 and classification == 1):
        return 1
    else:
        return 0

def create_single_sample():
    vec = []
    for att in attributes:
        # get the appropriate vector for each attribute and tie them together in the end
        rdm = getRandomValue(lengths[att], True)
        print(rdm)
        vec += rdm
    return vec + [2,2,2]

# a = create_single_sample()

# print(a)

    # # classification: 0 = female, 1 = male
    # classification = probe(sentence)
    # # get random gender as a fourth attribute (in the end of the vector) as a one-hot-encoding with two dimensions: [female, male]
    # gender_vec = getRandomValue(2, allow_zero=False)
    # vec = [*vec, *gender_vec]
    # # if the sampled gender is equal the classification (correctly classified) then we return 1 as 'is valid sentence' 
    # # if sampled gender and classification don't match, the sample is not valid and we return 0 as a label
    # label = get_label(classification, gender_vec)
    # return (vec,label)


# print(True == 1)
hypspace = 4*4*4*4*2
# hypspace = 1050
print(hypspace)
ja = int ( (1/0.2) * log( (Pow(2,hypspace) / 0.1), 2))

print(ja)