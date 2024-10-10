with open("mThesisCode/data.txt") as f:
    male = []
    female = []
    i = 0
    for line in f:
        line = line[:-2]
        # line = line.replace(",", ".")
        if i % 2 == 0:
            male.append(line)
        else:
            female.append(line)
        i += 1


for x in female:
    print(x)