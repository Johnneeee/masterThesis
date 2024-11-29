from sympy import *
import functools
import random

def define_variables(number):
    s = "".join(['v'+str(i)+',' for i in range(number)])
    V = [e for e in symbols(s)]
    return V

def generate_target(V, n_clauses,n_body_literals=-1):
    T = set()
    for i in range(n_clauses):
        if n_body_literals < 0:
            V_sample = random.sample(V, random.randint(1, len(V)-1))
        else:
            V_sample = random.sample(V, n_body_literals)
        clause = functools.reduce(lambda x,y: x & y, V_sample)
        V_implies = [item for item in V if item not in V_sample]
        x = random.randint(0, len(V)+1)
        target = ((clause) >> false if x == 0
                  else true >> (clause) if x == len(V)+1 and len(V_sample) == 1
                  else (clause) >> random.choice(V_implies))
        T.add(target)
    return T


def evalFormula(formula, x, V):
    """
        eg:
            input = (
                    Implies(v0, v1),
                    [1, 1, 0, 0],
                    [v0, v1, v2, v3],
                    )
            output = True (True if formula holds according to the example x, else False )
    """
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
    """
        sorting (weird kind of sorting) and formatting set to theory
        eg:
            input = {Implies(v1 & v2, v3), Implies(v0, v1)}
            output = (Implies(v0, v1)) & (Implies(v1 & v2, v3))
    """ 
    tempt = True
    for e in set:
        tempt = tempt & e
        
    return tempt

def entails(T,clause,V):
    '''
    Checks if T entails a horn clause c.
    Returns an assignment that falsifies c and satisfies T
     if the check is false.
    '''
    T1 = set2theory(T)
    assignment =satisfiable(T1 & ~clause)
    res =[0 for i in range(len(V))]
    if assignment != False :
        for e in assignment:
            idx = V.index(e)
            res[idx] =  1 if assignment[e] == True else 0
        return res
    return True

def EQ(H, V, T):
    for clause in H:
        answer = entails(T,clause,V)
        if  answer != True:
            #here a positive counterexample is returned
            return answer
    for clause in T:
        answer = entails(H,clause,V)
        if  answer != True:
            #here a negative counterexample is returned
            return answer
    return True

def MQ(clause, V, T):
    T = set2theory(T)
    return evalFormula(T, clause, V)

def get_hypothesis(S, V):
    H = set()
    for a in S:
        L = [V[index] for index,value in enumerate(a) if a[index] == 1] + [true] # antecedant
        R = [V[index] for index,value in enumerate(a) if a[index] == 0] + [false] # consequent
        for r in R:
            clause = functools.reduce(lambda x,y: x & y, L) #[v0 v2 v3] -> v0 & v1 & v3
            clause = (clause) >> r
            H.add(clause)
    return H


def learn(V,iterations=-1):
    H = set()
    S = []
    i = 0

    while True and iterations!=0:
        counterExample = EQ(H, V, T)
        
        #If EQ(H) returns True
        if counterExample == True:
            print("terminating")
            return H

        pos_ex = False

        # If counterExample is positive
        for clause in H.copy():
            if (evalFormula(clause, counterExample, V) == False):
                pos_ex = True
                H.remove(clause)
                
        # If counterExample is negative
        if not pos_ex:
            replaced = False
            for s in S:
                s_intersection_x = [1 if s[index] ==1 and counterExample[index] == 1 else 0 for index in range(len(V))]
                A = {index for index,value in enumerate(s_intersection_x) if value == 1}
                B = {index for index,value in enumerate(s) if value == 1 }
                if A.issubset(B) and not B.issubset(A): # A properly contained in B
                    idx = S.index(s)
                    if MQ(s_intersection_x, V, T) == False and s_intersection_x:
                        S[idx] = s_intersection_x
                        replaced = True
                        break
            if not replaced:
                S.append(counterExample)
            H = get_hypothesis(S,V)

        #logging
        i += 1
        sentence = f"iteration {i}, len(H) = {len(H)}"
        print(sentence)

    return H


V = define_variables(4) # our vocabulary V

#Generating random target
T = generate_target(V, 2) # the target concept T ### we dont know this in practice

# Setting known target
# T = {Implies(V[0], V[1]), Implies(V[1] & V[2], V[3])}

finalH = learn(V, iterations=10)

print("")
print(f"Target = {T}")
print(f"Final Hyp = {finalH}")