from sympy import *
import functools
import random
import timeit
from intepretor import *


def probe(unmasker, sentence, model = 'roberta-base'):
    if model.split('-')[0] == 'bert' :
        sentence = sentence.replace('<mask>', '[MASK]')
    result = unmasker(sentence)

    for reply in result: # for the replies returned by the language model
        #if female
        if (reply["token_str"]).lower() == "hun" or (reply["token_str"]).lower() == "ho": # i should add more cases
            return 0
        #if male
        if (reply["token_str"]).lower() == "han": # i should add more cases
            return 1
        else:

            continue
    return result[0]['token_str']

def get_eq_sample_size(epsilon=0.2, delta=0.1):
    H = 1080 # number of possible examples
    return int ( (1/epsilon) * log( (Pow(2,H) / delta), 2))

def get_random_sample(length, allow_zero = True, amount_of_true=1):
    vec = np.zeros(length, dtype=np.int8)
    # allow for all zeroes: one extra sample length and if its out of index range, use all zeroes vector (equal possibility)
    if allow_zero:
        idx = random.sample(range(length + 1), k=amount_of_true)
    else:
        idx = random.sample(range(length), k=amount_of_true)
    for i in idx:
        if i < length:
            vec[i] = 1
    return list(vec)

def get_label(classification, gender):
    """
        Does handling no 1 in vector work as a diverse attribute (neither he or she) to include they?
        -> never gets predicted so what rules result from that? Influences other attributes?
    """
    if (gender[0] == 1 and classification == 0) or (gender[1] == 1 and classification == 1):
        return 1
    else:
        return 0

def create_single_sample(template, attributes, lm : str, intepretor : Intepretor, unmasker):
    vec = []
    for att in attributes:
        # get the appropriate vector for each attribute and tie them together in the end
        vec = [*vec, *get_random_sample(intepretor.lengths[att], allow_zero=True)]
    sentence = intepretor.binaryToSentence(vec, template)
    # classification: 0 = female, 1 = male
    classification = probe(unmasker, sentence, model=lm)
    # get random gender as a fourth attribute (in the end of the vector) as a one-hot-encoding with two dimensions: [female, male]
    gender_vec = get_random_sample(2, allow_zero=False)
    vec = [*vec, *gender_vec]
    # if the sampled gender is equal the classification (correctly classified) then we return 1 as 'is valid sentence' 
    # if sampled gender and classification don't match, the sample is not valid and we return 0 as a label
    label = get_label(classification, gender_vec)
    return (vec,label)

def evalFormula(formula, x, V):
    if formula == true:
        return True
    if formula == false:
        return False
    a = {V[i]: x[i] for i in range(len(V))}
    for i in range(len(V)):
        a[V[i]] = (True if x[i] == 1
                        else False)
    return True if formula.subs(a) == True else False

def set2theory(set):
    tempt = True
    for e in set:
        tempt = tempt & e
    return tempt

def custom_EQ(template,attributes, H, lm, unmasker, V, bad_nc, intepretor : Intepretor):
    h = true
    if len(H):
        h = set2theory(H)
    for i in range(get_eq_sample_size()):
        (a,l) = create_single_sample(template,attributes, lm, intepretor, unmasker)
        if l == 0 and evalFormula(h,a,V) and a not in bad_nc:
            #print("Sample number", i+1)
            return (a, i+1)
        if l == 1 and not evalFormula(h,a,V):
            #print("Sample number ", i+1)
            return (a, i+1)
    return True

def custom_MQ(template,assignment, lm, unmasker, intepretor : Intepretor):
    vec = assignment[:-2]
    genderVec = assignment[-2:]
    sentence = intepretor.binaryToSentence(vec, template)
    classification = probe(unmasker, sentence, model=lm)
    label = get_label(classification, genderVec)
    res  = ( True if label == 1
                else False)
    return res

def get_hypothesis(S, V,bad_nc,background):
    H = set()
    for a in [a for a in S if a not in bad_nc]:
        L = [V[index] for index,value in enumerate(a) if a[index] == 1] + [true]
        R = [V[index] for index,value in enumerate(a) if a[index] == 0] + [false]
        for r in R:
            clause = functools.reduce(lambda x,y: x & y, L)
            clause = (clause) >> r
            H.add(clause)
    H = H.union(background)
    return H

def refineHyp(H,S,Pos,V,bad_nc):
    #small optimisation. Refine hypo. with known positive counterexamples.
    for pos in Pos:
        for clause in H.copy():
            if (evalFormula(clause, pos, V) == False):
                H.remove(clause)
                # identify_problematic_nc(H,S,bad_nc)

    identify_problematic_nc(H,S,bad_nc,V)
    return H

def identify_problematic_nc(H,S,bad_nc,V):
    #check if a nc in S does not falsify a clause in H
    h=set2theory(H)
    for a in [a for a in S if a not in bad_nc]:
        if (evalFormula(h, a, V) == True):
            bad_nc.append(a)

def checkDup(list,a,bad_nc):
    if a in list:
        bad_nc.append(a)
        return True
    
    return False

def hornAlgorithm(V,MQ,EQ, bad_nc,bad_pc,background= {},iterations=-1):
    terminated = False
    metadata = []
    H = set()
    H = H.union(background)
    S = []
    i = 0
    #remember positive counterexamples
    Pos = []
    #list of negative counterexamples that cannot produce a rule (according to positive counterexamples)
    #bad_nc =[]
    while True and iterations!=0:
        data = {}
        start = timeit.default_timer()
        #Ask for H
        eq_res = EQ(H)
        if eq_res == True:
            terminated = True
            stop = timeit.default_timer()
            data['runtime'] = stop-start
            metadata.append(data)
            with open('output.txt', 'a') as f:
                f.write("=== TERMINATED ===\n")
            return (terminated, metadata, H)

        (counterEx,sampleNr) = eq_res
        data['sample'] = sampleNr
        pos_ex=False

        # if EQ() returns a positive counterexample
        for clause in H.copy():
            if (evalFormula(clause, counterEx,V) == False):
                if clause in background:
                    bad_pc.append(counterEx)
                else:
                    H.remove(clause)
                    Pos.append(counterEx)
                    identify_problematic_nc(H,S,bad_nc,V)
                    pos_ex = True
                    
        # if EQ() returns a positive counter example
        if not pos_ex:
            replaced = False
            for s in S:
                s_intersection_x = [1 if s[index] ==1 and counterEx[index] == 1 else 0 for index in range(len(V))]
                A = {index for index,value in enumerate(s_intersection_x) if value ==1}
                B = {index for index,value in enumerate(s) if value ==1}
                if A.issubset(B) and not B.issubset(A): # A properly contained in B
                    idx = S.index(s)
                    if MQ(s_intersection_x) == False and s_intersection_x not in bad_nc:
                        if not checkDup(S,s_intersection_x,bad_nc):
                            S[idx] = s_intersection_x
                            replaced = True
                        break
            if not replaced:
                S.append(counterEx)

            H = get_hypothesis(S,V,bad_nc,background)
            H = refineHyp(H,S,Pos,V,bad_nc)

        # logging
        iterations-=1
        stop = timeit.default_timer()
        data['runtime'] = stop-start
        metadata.append(data)
        i += 1
        print(f"iteration = {i}, len(H) = {len(H)}, runTime = {[data['runtime']]}")

        # if iterations % 5 == 0:
        #     log = f"iteration = {i}, len(H) = {len(H)}, rt = {[data['runtime']]}"
        #     with open('output.txt', 'a') as f:
        #         f.write(log)
    return (terminated, metadata, H)



