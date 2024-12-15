

import pickle
import csv

ja = [1,2,3,4]
V = {ja[0],ja[1],ja[2],ja[3], ja[0]}
print(V)
with open('testcsv' + '.txt', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(V) 

with open('testcsv' + '.txt', 'r') as file:
      
  # reading the CSV file  
  csvFile = csv.reader(file)  
    
  # displaying the contents of the CSV file  
  for lines in csvFile:  
        print(lines)  



# print(W)
# print(W[0])
