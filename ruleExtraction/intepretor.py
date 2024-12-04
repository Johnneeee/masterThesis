import pandas as pd
import numpy as np
import random
import csv

class Intepretor:
    def __init__(self, attributes, filePaths, neutralCases, template):
        self.lookTable = self.formatLookupTable(attributes, filePaths, neutralCases)
        self.template = template
        self.lengths = {i[0]:len(i[1][0]) for i in self.lookTable.items()}

    def formatLookupTable(self, attributes, filePaths, neutralCases):
        # {attribute: ([attributes], neutralCase)}
        # ['occupation': (['sykepleier', 'helsefagarbeider', 'adjunkt', 'barnehagelærer', 'mekaniker', 'elektriker', 'betongfagarbeider', 'sveiser'], 'person')},]
        lookup = {}
        for i in range(len(attributes)):
            data = []
            with open(filePaths[i], mode ='r', encoding="UTF-8") as f:
                next(f)
                csvFile = csv.reader(f)
                for lines in csvFile:
                    data.append(lines[0])
            lookup[attributes[i]] = (data, neutralCases[i])
                # print(data)
        return lookup

    def binaryToAttribute(self, type, bin):
        attributeLookup = self.lookTable[type]
        nonzero = np.nonzero(bin)[0]
        if len(nonzero) > 0:
            index = nonzero[0]
            return attributeLookup[0][index]
        else:
            return attributeLookup[1]


    def binaryToSentence(self, bin, template : str):
        # [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0]
        # <mask> er yngre enn 20 år og er en elektriker fra Stavanger med bakgrunn fra Afrika.

        attributes = []
        splitIndexes = []

        i = 0
        for x in self.lookTable.items():
            attributes.append(x[0])
            splitIndexes.append(len(x[1][0]) + i)
            i += len(x[1][0])

        bin = np.array(bin)
        splitted = np.split(bin, splitIndexes)
        
        # [('age', array([1, 0, 0, 0, 0, 0])), ('occupation', array([0, 0, 0, 0, 1, 0, 0, 0])), ('city', array([0, 0, 0, 0, 0, 0, 1, 0])), ('ethnicity', array([0, 0, 0, 0, 1, 0]))]
        values = list(zip(attributes, splitted))

        # [['age', 'yngre enn 20'], ['occupation', 'mekaniker'], ['city', 'Bodø'], ['ethnicity', 'Europa']]
        values = list(map(lambda val: [val[0], self.binaryToAttribute(val[0],val[1])],values))
        for attribute, value in values:
            template = template.replace(f"[{attribute}]", value)

        # print(template)
        return template



#############################################################################
# import pandas as pd
# import numpy as np
# import random
# import csv

# class Intepretor:
#     def __init__(self, age_file, occ_file, cities_file, ethnicity_file):
#         self.age_lookup = self.fileToEnumDict(age_file)
#         self.occupation_lookup = self.fileToEnumDict(occ_file)
#         self.cities_lookup = self.fileToEnumDict(cities_file)
#         self.ethnicity_lookup = self.fileToEnumDict(ethnicity_file)
#         self.lengths = {'age' : len(self.age_lookup), 'occupation' : len(self.occupation_lookup), 'city' : len(self.cities_lookup), 'ethnicity' : len(self.ethnicity_lookup)}
    
#     def fileToEnumDict(self, fileName):
#         # "data/occupationValues.csv"
#         # -> {'Oslo': 0, 'Kristiansand': 1, 'Stavanger': 2, 'Bergen': 3, 'Ålesund': 4}
#         data = pd.read_csv(fileName).to_numpy().flatten()
#         return {data[i] : i for i in range(len(data))}

#     def binaryToAttribute(self, vector, type):
#         # [0 0 0 0 0 0], "age"
#         # -> "mellom 0 og 100"
#         lookup = self.get_lookup(type)
#         inv_lookup = {v: k for k, v in lookup.items()}
#         nonzero = np.nonzero(vector)
#         if len(nonzero[0]) > 0:
#             index = nonzero[0][0]
#             return inv_lookup[index]
#         else:
#             if type == "age":               #age
#                 return 'mellom 0 og 100'
#             elif type == 'occupation':      #occupation
#                 return 'person'
#             elif type == "city":            #city
#                 return 'en ukjent by'
#             elif type == "ethnicity":       #ethnicity 
#                 return "et ukjent sted"
    
#     def get_lookup(self, type):
#         # "age"
#         # -> {'sykepleier': 0, 'helsefagarbeider': 1, 'adjunkt': 2, 'barnehagelærer': 3, 'mekaniker': 4, 'elektriker': 5, 'betongfagarbeider': 6, 'sveiser': 7}
#         if type == 'age':
#             return self.age_lookup
#         elif type == 'occupation':
#             return self.occupation_lookup
#         elif type == 'city':
#             return self.cities_lookup
#         elif type == 'ethnicity':
#             return self.ethnicity_lookup
#         else:
#             return np.nan

#     def binaryToSentence(self, bin):
#         # [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0]
#         # -> <mask> er yngre enn 20 år og er en mekaniker fra Bodø med bakgrunn fra Europa
#         bin = np.array(bin)
#         i_age = len(self.age_lookup)
#         i_occupation = i_age + len(self.occupation_lookup)
#         i_city = i_occupation + len(self.cities_lookup)

#         splitted = np.split(bin, [i_age, i_occupation, i_city])

#         age = self.binaryToAttribute(splitted[0], type = "age")
#         occupation = self.binaryToAttribute(splitted[1], type = 'occupation')
#         city = self.binaryToAttribute(splitted[2], type = 'city')
#         ethnicity = self.binaryToAttribute(splitted[3], type = 'ethnicity')

#         sentence = "<mask> er {age} år og er en {occupation} fra {city} med bakgrunn fra {ethnicity}."
#         # print(sentence.format(age=age,city=city, occupation=occupation, ethnicity=ethnicity))
#         return sentence.format(age=age,city=city, occupation=occupation, ethnicity=ethnicity)
