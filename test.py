import matplotlib.pyplot as plt
import csv

def readData(path): # -> [[atts, yGold, yPred]]
    data = []
    with open(path, mode ='r', encoding="UTF-8")as file:
        csvFile = csv.reader(file, delimiter = ";")
        next(csvFile)
        for lines in csvFile:
            data.append([lines[0],float(lines[1]),float(lines[2])])

    data = sorted(data, key= lambda x: x[2], reverse=True) # sorted on pred ppbs low to high
    # data = data[::-1] # same order as censusdata
    
    return data


def plotdata(data, name):
    atts = [x[0] for x in data]
    yGold = [x[1] for x in data]
    yPred = [x[2] for x in data]
    y_positions = range(len(yGold))
    
    plt.figure(figsize=(10,70))
    
    plt.scatter(yGold, y_positions, color='green', label='gold')
    plt.scatter(yPred, y_positions, color='red', label='pred')
    
    # # Customize the y-axis to show only labels
    plt.yticks(ticks=y_positions, labels=atts)
    plt.ylim(-1,450)  
    
    # # Add labels, title, and legend
    plt.xlabel('PPBS')
    plt.ylabel('Occupations')
    plt.title(name)
    plt.legend()
    
    # grid
    plt.grid()
    plt.axvline(color='black')


data = readData("data/raw/xlmRBase_ppbs.csv") # read data from file
plotdata(data, "xlmRBase") # Plot the data
plt.show()