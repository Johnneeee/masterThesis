a = [['yngre enn 20 & mann ---> Afrika'],['yngre enn 20 & kvinne ---> Afrika'], ['yngre enn 20 & kvinne ---> Asia'], ['yngre enn 20 & kvinne ---> Australia'], ['yngre enn 20 & kvinne ---> Bergen'], ['yngre enn 20 & kvinne ---> Bodø'], ['yngre enn 20 & kvinne ---> Europa'], ['yngre enn 20 & kvinne ---> FALSE'], ['yngre enn 20 & kvinne ---> Kristiansand'], ['yngre enn 20 & kvinne ---> Nord Amerika'], ['yngre enn 20 & kvinne ---> Oslo'], ['yngre enn 20 & kvinne ---> Stavanger'], ['yngre enn 20 & kvinne ---> Sør Amerika'], ['yngre enn 20 & kvinne ---> Tromsø'], ['yngre enn 20 & kvinne ---> Trondheim'], ['yngre enn 20 & kvinne ---> arkitekt'], ['yngre enn 20 & kvinne ---> elektriker'], ['yngre enn 20 & kvinne ---> frisør'], ['yngre enn 20 & kvinne ---> politiker'], ['yngre enn 20 & kvinne ---> psykolog'], ['yngre enn 20 & kvinne ---> rørlegger'], ['yngre enn 20 & kvinne ---> sveiser'], ['yngre enn 20 & kvinne ---> sykepleier'], ['yngre enn 20 & kvinne ---> Ålesund']]
neg = [x[0][:-11] for x in a if x[0][-11:] == " ---> FALSE"]
f = []
print(neg)

f = [x for x in a if (x[0][-5:] == "FALSE") or (x[0].split(" ---> ")[0]) not in neg]
# for x in a:
#     # print(x)
#     if x[0][-5:] == "FALSE" or (x[0].split(" ---> ")[0]) not in neg:
#         f.append(x)
    # if (x[0].split(" ---> ")[0]) not in neg:
    #     f.append(x)
    # print(x[0].split(" ---> ")[0])

    # if (x[0][:-11] not in neg):
    #     f.append(x)
# f = list(filter(lambda x: [f"{x[0].split(' ---> ')[0]} ---> FALSE"] not in neg, a)) # drops false -> x
# f += neg
# for x in a:
#     print(x[0][-11:])


print(f)