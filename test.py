# with open("mThesisCode/data.txt") as f:
#     male = []
#     female = []
#     i = 0
#     for line in f:
#         line = line[:-2]
#         # line = line.replace(",", ".")
#         if i % 2 == 0:
#             male.append(line)
#         else:
#             female.append(line)
#         i += 1


# for x in female:
#     print(x)

import csv

lst = []
with open('utdanningnoLikestilling2023.csv', encoding="UTF-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    next(reader)
    # with open('occupationsNorge.csv', 'w', encoding="UTF-8") as rcsvfile:
    #         writer = csv.writer(rcsvfile, delimiter=';')
    for row in reader:
        lst.append([row[0]])
                # writer.writerows(row[0])
                # break
    # for row in reader:
    #     print(row[0])
        # break
with open('occupationsNorge.csv', 'w', encoding="UTF-8", newline="") as rcsvfile:
    writer = csv.writer(rcsvfile)
    writer.writerows(lst)


             
print(lst[:10])