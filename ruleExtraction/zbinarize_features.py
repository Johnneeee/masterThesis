import pandas as pd
import numpy as np
import random
import csv

class Binarizer: 
    """
        Takes care of converting a datapoint of the given dataset to a binary vector and vice-versa. The conversion is 
        a necessary step in using the rule-extractor with a language model. The relevant direction is here: converting a binary vector 
        into a sentence for the language model.

        Binary senquences represent: [AGE -- OCCUPATION -- CITY -- ETHNICITY] int this order.

        Parameters: country_file : str
                        The file-path to import the countries with their corresponding continents
                    # amount_containers : int
                    #     The amount of containers to be used to initialize the age containers. The containers are initialized
                    #     according to the total list of birth-dates divided into the given amount of intervals.
                    # occupation : int or str
                    #     Given that occ_file=True, this expects a file-path to directly import a list of occupations to binarize from a .csv
                    #     that has each occupation written in a seperate line. With occ_file=False this expect an integer value to determine the 
                    #     threshold above which an occupation is included based on the dataset total amounts.
    """
    def __init__(self, age_file, occ_file, cities_file, ethnicity_file):
        self.age_lookup = self.fileToEnumDict(age_file)
        self.occupation_lookup = self.fileToEnumDict(occ_file)
        self.cities_lookup = self.fileToEnumDict(cities_file)
        self.ethnicity_lookup = self.fileToEnumDict(ethnicity_file)
        self.lengths = {'age' : len(self.age_lookup), 'occupation' : len(self.occupation_lookup), 'city' : len(self.cities_lookup), 'ethnicity' : len(self.ethnicity_lookup)}
    
    def fileToEnumDict(self, fileName):
        """
            eg:
                input = fileToEnumDict(self, "data/occupationValues.csv")
                output = {'Oslo': 0, 'Kristiansand': 1, 'Stavanger': 2, 'Bergen': 3, 'Ålesund': 4}
        """
        data = pd.read_csv(fileName).to_numpy().flatten()
        return {data[i] : i for i in range(len(data))}

    # def binarize_string(self, input : str, kind):
    #     lookup = self.get_lookup(kind)
    #     vector = np.zeros(len(lookup), dtype=np.int8)
    #     vector[lookup[input]] = 1
    #     return vector
    
    def binary_to_string(self, vector, kind):
        """
            eg:
            input = binary_to_string(self, [0 0 0 0 0 0], "age")
            output = "mellom 0 og 100"
        """
        lookup = self.get_lookup(kind)
        inv_lookup = {v: k for k, v in lookup.items()}
        nonzero = np.nonzero(vector)
        if len(nonzero[0]) > 0:
            index = nonzero[0][0]
            return inv_lookup[index]
        else:
            if kind == "age":               #age
                return 'mellom 0 og 100'
            elif kind == 'occupation':      #occupation
                return 'person'
            elif kind == "city":            #city
                return 'en ukjent by'
            elif kind == "ethnicity":       #ethnicity 
                return "et ukjent sted"
    
    def get_lookup(self, label : str):
        """
            eg: 
            input = get_lookup(self, "age")
            output = {'sykepleier': 0, 'helsefagarbeider': 1, 'adjunkt': 2, 'barnehagelærer': 3, 'mekaniker': 4, 'elektriker': 5, 'betongfagarbeider': 6, 'sveiser': 7}
        """
        if label == 'age':
            return self.age_lookup
        elif label == 'occupation':
            return self.occupation_lookup
        elif label == 'city':
            return self.cities_lookup
        elif label == 'ethnicity':
            return self.ethnicity_lookup
        else:
            return np.nan

    def sentence_from_binary(self, bin):
        """
            eg:
            input = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0]
            output = <mask> er yngre enn 20 år og er en elektriker fra Stavanger med bakgrunn fra Afrika.
        """
        bin = np.array(bin)
        i_age = len(self.age_lookup)
        i_occupation = i_age + len(self.occupation_lookup)
        i_city = i_occupation + len(self.cities_lookup)

        splitted = np.split(bin, [i_age, i_occupation, i_city])

        age = self.binary_to_string(splitted[0], kind = "age")
        occupation = self.binary_to_string(splitted[1], kind = 'occupation')
        city = self.binary_to_string(splitted[2], kind = 'city')
        ethnicity = self.binary_to_string(splitted[3], kind = 'ethnicity')

        sentence = "<mask> er {age} år og er en {occupation} fra {city} med bakgrunn fra {ethnicity}."
        # print(sentence.format(age=age,city=city, occupation=occupation, ethnicity=ethnicity))
        return sentence.format(age=age,city=city, occupation=occupation, ethnicity=ethnicity)
