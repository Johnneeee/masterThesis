import pickle
# from sympy import *
# from binarize_features import *
import numpy as np
import json
import pandas as pd
# from intepretor import *

# data/rule_extraction/' + lm + '_rules_' + str(iterations) + '.txt'
with open('data/rule_extraction/' + "bert-base-multilingual-cased" + '_rules_' + "22" + '.txt', 'rb') as f:
    h = pickle.load(f)

with open('data/background.txt', 'rb') as f:
    background = pickle.load(f)



# print(h)
# print(background)
def get_all_rules(h, background):
    all_rules = []
    for rule in h:
        if rule not in background:
            expr = str(rule)
            all_rules.append(expr)
            # all_rules.append(rule)
    return all_rules

# allRules = get_all_rules(h,background)
# print(allRules)

def make_rule_lists(all_rules): # &ant -> con
    rules = []
    negations = []
    implications = []
    for rule in all_rules:
        if '~' in rule:
            idx = []
            if not '(' in rule:
                idx.append(int(rule.replace('~v', '')))
            else:
                for s in rule.split(' '):
                    if 'v' in s:
                        s = s.replace('~(', '')
                        s = s.replace(')', '')
                        idx.append(int(s.replace('v', '')))
            rules.append({'con' : '','ant' : idx})
            negations.append(idx)
        else:
            ant, con = rule.split(', ')
            ant_idx = []
            for s in ant.split(' '):
                if 'v' in s:
                    s = s.replace('Implies(', '')
                    ant_idx.append(int(s.replace('v', '')))
            con_idx = con.replace('v', '').replace(')','')
            rules.append({'con' : con_idx, 'ant' : ant_idx})
            implications.append({'con' : con_idx, 'ant' : ant_idx})
    return (rules, negations, implications)


def negation_to_string(rule, total_lookup): # [1,2] -> not (ja & nei)
    s = "not ("
    for variable in rule:
        # print(variable)
        s = s + total_lookup[variable] + " & "
    s = s[:-2]
    s = s + ")"
    return s

# negToString = negation_to_string(negations[0], lookupTable)
# print(negToString)

# def negation_to_latex(rule, total_lookup): #[1,2] -> \text{ja} \land \text{nei}  \rightarrow \bot$
#     s = ""
#     for variable in rule:
#         s = s + "\\text{" + total_lookup[variable] + "} \\land "
#     s = s[:-6]
#     s = s + " \\rightarrow \\bot$"
#     return s

# negToLatex = negation_to_latex(negations[0], lookupTable)
# print(negToLatex)

def get_negation_strings(negations, total_lookup):
    negations_strings = []
    for rule in negations:
        negations_strings.append(negation_to_string(rule, total_lookup))
    return negations_strings

# negationStrings = get_negation_strings(negations, lookupTable)
# print(negationStrings)

def implication_to_string(rule, total_lookup):
    s = ""
    for variable in rule['ant']:
        s = s + total_lookup[variable] + " & "
    s = s[:-2]
    s = s + " ---> " + total_lookup[int(rule['con'])]
    return s

# implicationNr = implications[2]
# implicationToString = implication_to_string(implicationNr, lookupTable)
# print(implicationNr)
# print(implicationToString)

# def implication_to_latex(rule, total_lookup):
#     s = ""
#     for variable in rule['ant']:
#         s = s + "\\text{" + total_lookup[variable] + "} \\land "
#     s = s[:-6]
#     s = s + " \\rightarrow \\text{" + total_lookup[int(rule['con'])] + "} $"
#     return s

# def get_relevant_implications(implications, negations, total_lookup): # it filters out false -> b bc we dont care
#     implication_strings = []
#     for rule in implications:
#         if rule['ant'] not in negations:
#             implication_strings.append(implication_to_string(rule, total_lookup))
#     return implication_strings

def get_relevant_implications2(implications, negations): # it filters out false -> b bc we dont care
    implication_strings = []
    for rule in implications:
        if rule['ant'] not in negations:
            implication_strings.append(rule)
    return implication_strings

# releImplications = get_relevant_implications(implications, negations, lookupTable)
# releImplications2 = get_relevant_implications2(implications, negations)
# print(releImplications)
# print(releImplications)
# def load_rules(lm, eq, e):
#     with open('data/rule_extraction/' + lm + '_rules_' + str(eq) + '.txt', 'rb') as f:
#         h = pickle.load(f)
#     return h

# def load_background():
#     with open('data/background.txt', 'rb') as f:
#         background = pickle.load(f)
#     return background

def count_lists(l): #count nr of rule occurrences
    counts = []
    sublists = []
    for sublist in l:
        if sublist not in sublists:
            counts.append([sublist, l.count(sublist)])
            sublists.append(sublist)
    return counts

# countImps = count_lists(implications)
# countReleImps = count_lists(releImplications2)
# countNeg = count_lists(negations)

def print_all_counted_rules(negations, implications, lookup):
    for rule, count in sorted(negations, key=lambda rule: rule[1], reverse=True):
            rule_string = negation_to_string(rule, lookup)
            print("{:.3f}  :  {rule}".format(count/10, rule=rule_string))
    for rule, count in sorted(implications, key=lambda rule: rule[1], reverse=True):
            rule_string = implication_to_string(rule, lookup)
            print("{:.3f}  :  {rule}".format(count/10, rule=rule_string))

# print_all_counted_rules(countNeg, countReleImps, lookupTable)

def get_data_dict(lm, eq, e):
    with open('data/rule_extraction/{lm}_metadata_{eq}_{experiment}.json'.format(lm=lm, eq=eq, experiment=e)) as f:
        data = f.read()
    return json.loads(data)

def make_sample_df(sample_list, eq=0):
    sample_list = [[sample['sample'], sample['runtime']] for sample in sample_list ]
    iteration_arr = np.reshape(np.arange(1, len(sample_list)), (len(sample_list), 1))
    sample_list_mod = np.append(sample_list, iteration_arr, axis=1)
    if eq == 0:
        return pd.DataFrame(sample_list_mod, columns=['samples', 'runtime', 'iteration'])
    else:
        eq_arr = np.zeros_like(iteration_arr)
        eq_arr.fill(eq)
        sample_list_mod = np.append(sample_list_mod, eq_arr, axis=1)
        return pd.DataFrame(sample_list_mod, columns=['samples', 'runtime', 'iteration', 'eq'])
    
######################################################################################################################
# import pickle
# from sympy import *
# from binarize_features import *
# import json
# import pandas as pd

# def get_all_rules(h, background):
#     all_rules = []
#     for rule in h:
#         if rule not in background:
#             expr = sstr(rule)
#             all_rules.append(expr)
#             #print(expr)
#     return all_rules

# def make_rule_lists(all_rules):
#     rules = []
#     negations = []
#     implications = []
#     for rule in all_rules:
#         if '~' in rule:
#             idx = []
#             if not '(' in rule:
#                 idx.append(int(rule.replace('~v', '')))
#             else:
#                 for s in rule.split(' '):
#                     if 'v' in s:
#                         s = s.replace('~(', '')
#                         s = s.replace(')', '')
#                         idx.append(int(s.replace('v', '')))
#             rules.append({'head' : '','body' : idx})
#             negations.append(idx)
#         else:
#             body, head = rule.split(', ')
#             body_idx = []
#             for s in body.split(' '):
#                 if 'v' in s:
#                     s = s.replace('Implies(', '')
#                     body_idx.append(int(s.replace('v', '')))
#             head_idx = head.replace('v', '').replace(')','')
#             rules.append({'head' : head_idx, 'body' : body_idx})
#             implications.append({'head' : head_idx, 'body' : body_idx})
#     return (rules, negations, implications)

# # def get_lookup(binarizer):
# #     total_lookup = []
# #     for v in binarizer.age_lookup.keys():
# #         total_lookup.append(v)
# #     for v in binarizer.occupation_lookup.keys():
# #         total_lookup.append(v)
# #     for v in binarizer.cities_lookup.keys():
# #         total_lookup.append(v)
# #     for v in binarizer.ethnicity_lookup.keys():
# #         total_lookup.append(v)
# #     total_lookup.append('kvinne')
# #     total_lookup.append('mann')
# #     #print({i : total_lookup[i] for i in range(len(total_lookup))})
# #     return total_lookup

# def negation_to_string(rule, total_lookup):
#     s = "not ("
#     for variable in rule:
#         s = s + total_lookup[variable] + " & "
#     s = s[:-2]
#     s = s + ")"
#     return s

# def negation_to_latex(rule, total_lookup):
#     s = ""
#     for variable in rule:
#         s = s + "\\text{" + total_lookup[variable] + "} \\land "
#     s = s[:-6]
#     s = s + " \\rightarrow \\bot$"
#     return s

# def get_negation_strings(negations, total_lookup):
#     negations_strings = []
#     for rule in negations:
#         negations_strings.append(negation_to_string(rule, total_lookup))
#     return negations_strings

# def implication_to_string(rule, total_lookup):
#     s = ""
#     for variable in rule['body']:
#         s = s + total_lookup[variable] + " & "
#     s = s[:-2]
#     s = s + " ---> " + total_lookup[int(rule['head'])]
#     return s

# def implication_to_latex(rule, total_lookup):
#     s = ""
#     for variable in rule['body']:
#         s = s + "\\text{" + total_lookup[variable] + "} \\land "
#     s = s[:-6]
#     s = s + " \\rightarrow \\text{" + total_lookup[int(rule['head'])] + "} $"
#     return s

# def get_relevant_implications(implications, negations, total_lookup):
#     implication_strings = []
#     for rule in implications:
#         if rule['body'] not in negations:
#             implication_strings.append(implication_to_string(rule, total_lookup))
#     return implication_strings

# def load_rules(lm, eq, e):
#     with open('data/rule_extraction/' + lm + '_rules_' + str(eq) + '.txt', 'rb') as f:
#         h = pickle.load(f)
#     return h

# def load_background():
#     with open('data/background.txt', 'rb') as f:
#         background = pickle.load(f)
#     return background

# def count_lists(l):
#     counts = []
#     sublists = []
#     for sublist in l:
#         if sublist not in sublists:
#             counts.append([sublist, l.count(sublist)])
#             sublists.append(sublist)
#     return counts

# def print_all_counted_rules(negations, implications, lookup):
#     for rule, count in sorted(negations, key=lambda rule: rule[1], reverse=True):
#             rule_string = negation_to_string(rule, lookup)
#             print("{:.3f}  :  {rule}".format(count/10, rule=rule_string))
#     for rule, count in sorted(implications, key=lambda rule: rule[1], reverse=True):
#             rule_string = implication_to_string(rule, lookup)
#             print("{:.3f}  :  {rule}".format(count/10, rule=rule_string))

# def get_data_dict(lm, eq, e):
#     with open('data/rule_extraction/{lm}_metadata_{eq}_{experiment}.json'.format(lm=lm, eq=eq, experiment=e)) as f:
#         data = f.read()
#     return json.loads(data)

# def make_sample_df(sample_list, eq=0):
#     sample_list = [[sample['sample'], sample['runtime']] for sample in sample_list ]
#     iteration_arr = np.reshape(np.arange(1, len(sample_list)), (len(sample_list), 1))
#     sample_list_mod = np.append(sample_list, iteration_arr, axis=1)
#     if eq == 0:
#         return pd.DataFrame(sample_list_mod, columns=['samples', 'runtime', 'iteration'])
#     else:
#         eq_arr = np.zeros_like(iteration_arr)
#         eq_arr.fill(eq)
#         sample_list_mod = np.append(sample_list_mod, eq_arr, axis=1)
#         return pd.DataFrame(sample_list_mod, columns=['samples', 'runtime', 'iteration', 'eq'])
    
#     # [{'sample': 2, 'runtime': 1.3905771999852732}, {'sample': 9, 'runtime': 2.119604499952402}]