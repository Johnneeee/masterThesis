import numpy as np
import csv

class Intepretor:
    def __init__(self, filePaths, template):
        self.lookupTable = self.formatLookupTable(filePaths)
        self.template = template
        self.lengths = {i[0]:len(i[1][0]) for i in self.lookupTable.items()}
        self.attributes = [x for x in self.lookupTable]
        self.splitIndexes = [sum(list(self.lengths.values())[:i+1]) for i in range(len(self.lengths))]

    def formatLookupTable(self, filePaths):
        # {attribute: ([values], neutralCase)}
        # ['occupation': (['sykepleier', 'helsefagarbeider', 'adjunkt', 'barnehagelærer', 'mekaniker', 'elektriker', 'betongfagarbeider', 'sveiser'], 'person')},]
        lookup = {}
        for i in range(len(filePaths)):
            data = []
            with open(filePaths[i], mode ='r', encoding="UTF-8") as f:
                # next(f)
                csvFile = csv.reader(f)
                for lines in csvFile:
                    data.append(lines[0])
            lookup[data[0]] = (data[1:-1], data[-1])
                # print(data)
        # print(lookup)
        return lookup

    def binaryToAttribute(self, type, bin):
        attributeLookup = self.lookupTable[type]
        nonzero = np.nonzero(bin)[0]
        if len(nonzero) > 0:
            index = nonzero[0]
            return attributeLookup[0][index]
        else:
            return attributeLookup[1]


    def binaryToSentence(self, bin):
        # [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0]
        # <mask> er yngre enn 20 år og er en elektriker fra Stavanger med bakgrunn fra Afrika.

        bin = np.array(bin)
        splitted = np.split(bin, self.splitIndexes)
        
        # [('age', array([1, 0, 0, 0, 0, 0])), ('occupation', array([0, 0, 0, 0, 1, 0, 0, 0])), ('city', array([0, 0, 0, 0, 0, 0, 1, 0])), ('ethnicity', array([0, 0, 0, 0, 1, 0]))]
        values = list(zip(self.attributes, splitted))[:-1]
        # print(values)

        # [['age', 'yngre enn 20'], ['occupation', 'mekaniker'], ['city', 'Bodø'], ['ethnicity', 'Europa']]
        values = list(map(lambda val: [val[0], self.binaryToAttribute(val[0],val[1])],values))

        template = self.template
        for attribute, value in values:
            template = template.replace(f"[{attribute}]", value)

        # print(template)
        return template
