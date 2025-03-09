# a = 4,4,5,4,4,4,5,3,3,4,4,4,4,3,3,4,4,6,4,3

# b = 4,8,2 # tillegg (real, alder, studie)


# bio1 = 0.5
# fys1 = 0.5
# kjem1 = 0.5
# kjem2 = 0.5
# it1 = 0.5
# r1 = 0.5
# r2 = 1
# print((sum(a)/len(a))*10 + sum(b))


ls = [0.98, 0.02, 0.336, 0.33, 0.026, 0.002, -0.412, 0.306, -0.284, -0.086, 0.072, -0.51, -0.114, -0.008, 0.028, 0.332, -0.378, -0.246, 0.008, -0.368]

ls.sort(reverse=True)

# fstNeg = None
# fstPos = None

for i in range(len(ls)):
    if ls[i] > 0:
        print(i-0.5) 
        break