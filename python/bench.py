from d3crypt0r import *



def analyze(cipher):
    enemies = [set() for _ in range(T)]
    for i,c in enumerate(cipher):
        if i>0:
            cprev = cipher[i-1]
            enemies[c].add(cprev)
            enemies[cprev].add(c)
        if i<len(cipher)-1:
            cnxt = cipher[i+1]
            enemies[c].add(cnxt)
            enemies[cnxt].add(c)
    for i,e in enumerate(enemies):
        print(f"If {i} is <space>, {T-len(e)} other possible for <space>")

def is_addmissible(cipher,ptxt):
    k = dict()
    ktbl = dict()
    for a in alphabet:
        k[a] = set()
    for i,c in enumerate(cipher):
        if i>=len(ptxt):
            return True
        pc = ptxt[i]
        k[pc].add(c)
        if c not in ktbl:
            ktbl[c] = pc
        else:
            c_map = ktbl[c]
            if c_map != pc:
                return False
        if len(k[pc])>rowlen_d[pc]:
            return False
    return True

def ad_number(cipher,ptxt):
    k = dict()
    ktbl = dict()
    for a in alphabet:
        k[a] = set()
    for i,c in enumerate(cipher):
        if i>=len(ptxt):
            return -1
        pc = ptxt[i]
        k[pc].add(c)
        if c not in ktbl:
            ktbl[c] = pc
        else:
            c_map = ktbl[c]
            if c_map != pc:
                return i
        if len(k[pc])>rowlen_d[pc]:
            return i
    return -1

pts = [gen_random_plaintxt() for _ in range(40)]
rkey = gen_key()
ciphs = [encrypt(x,rkey) for x in pts]
# analyze(ciph)
ts = []

for i,pl in enumerate(pts):
    for j,ci in enumerate(ciphs):
        if i==j:
            continue
        ts.append(ad_number(ci,pl))

import matplotlib.pyplot as plt
# for x in stats.keys():
#     plt.hist(stats[x],bins=20,label=x,alpha=0.5)

# plt.legend()
# plt.show()

plt.hist(ts,bins = 30)
plt.legend()
plt.title('characters consumed until inconsisitency')
plt.xlabel('characters consumed')
plt.show()




# JWORDS = 7
# words = get_words()
# N = len(words)
# stts = []
# # N = 4

# addmissible_states = []
# for t in range(len(words)**JWORDS):
#     stt = [0 for _ in range(JWORDS)]
#     for j in range(JWORDS):
#         stt[j] = (t//(N**j))%N
#     # print(stt)
#     ptxt = ""
#     for i in range(JWORDS):
#         ptxt+=words[stt[i]]+" "
#     # print(ptxt)
#     if is_addmissible(ciph,ptxt):
#         addmissible_states.append(stt)
#         print(stt)

# print(len(addmissible_states))
    