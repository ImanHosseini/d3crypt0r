import json
stats:dict = json.load(open("./stats.txt","r"))
# print(stats)

import matplotlib.pyplot as plt
# for x in stats.keys():
#     plt.hist(stats[x],bins=20,label=x,alpha=0.5)

# plt.legend()
# plt.show()

ds = []
dl = []
for x in stats.keys():
    ds.append(stats[x])
    dl.append(x)

plt.hist(ds,bins = 25,label=dl)
plt.legend()
plt.title('execution time histogram per arch-compiler')
plt.xlabel('executaion time (ns)')
plt.show()