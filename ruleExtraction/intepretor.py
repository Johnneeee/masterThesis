import numpy as np
import csv

class Intepretor:
    def __init__(self, attributes, filePaths, neutralCases, template):
        self.lookTable = self.formatLookupTable(attributes, filePaths, neutralCases)
        self.template = template
        self.lengths = {i[0]:len(i[1][0]) for i in self.lookTable.items()}
        self.attributes = attributes

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


    def binaryToSentence(self, bin):
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
        template = self.template
        for attribute, value in values:
            template = template.replace(f"[{attribute}]", value)

        # print(template)
        return template
