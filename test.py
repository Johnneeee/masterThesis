
ja = [(1,3), (3,1), (1,2), (1,4)]

ja = sorted(ja, key=lambda x: max(x[0], x[1]))

print(ja)