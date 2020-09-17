import random

alphabet = " abcdefghijklmnopqrstuvwxyz"
T = 106 # Sum(rowlen)
rowlen = [19,7,1,2,4,10,2,2,5,6,1,1,3,2,6,6,2,1,5,5,7,2,1,2,1,2,1]
rowlen_d = dict()
for i,rl in enumerate(rowlen):
    rowlen_d[alphabet[i]] = rl

def gen_random_plaintxt():
    L = 500
    ptxt = ""
    words = []
    with open("./data/words.txt") as wordsf:
        words = [x.strip().lower() for x in wordsf.readlines()]
        words = list(filter(lambda x: "'" not in x,words))
        # print(len(words))
    curs = 0
    print(len(words))
    while(curs<L-3):
        w = words[random.randint(0,len(words)-1)]
        ptxt = ptxt + w +" "
        curs += len(w)
    # Kill trailing space
    ptxt = ptxt[:-1]
    return ptxt

def default_sched(j,llen,L=0):
    return j % llen

# Key is hashmap < alphabet , list < int > >
def gen_key():
    key = dict()
    ci_alpha = list(range(T))
    for i in range(len(alphabet)): 
        random.shuffle(ci_alpha)
        key[alphabet[i]] =  ci_alpha[:rowlen[i]]
        ci_alpha = ci_alpha[rowlen[i]:]
    # print(key)
    return key

def encrypt(plain_txt,key,sched = default_sched):
    cipher_ = []
    for j,c in enumerate(plain_txt):
        cipher_.append(key[c][sched(j,rowlen_d[c])])
    # print(cipher_)
    return cipher_

def decrypt(cipher,key:dict):
    ptxt = ""
    for i,c in enumerate(cipher):
        for k in key.items():
            plain_c = k[0]
            plist = k[1]
            if c in plist:
                ptxt += plain_c
                break
    return ptxt

# given a cipher and a plaintxt check if its possible that they're same
def checker(cipher,ptxt):
    k = dict()
    for a in alphabet:
        k[a] = set()
    for i,c in enumerate(cipher):
        pc = ptxt[i]
        k[pc].add(c)
        if len(k[pc])>rowlen_d[pc]:
            print(f"NOT SAME! CAUGHT AT {i}")
            return

k = gen_key()
ptxt1 = gen_random_plaintxt()
ptxt2 = gen_random_plaintxt()
cipher1 = encrypt(ptxt1,k)
cipher2 = encrypt(ptxt2,k)
checker(cipher1,ptxt2)


# k = gen_key()
# ptxt = gen_random_plaintxt()
# print(ptxt)
# cipher = encrypt(ptxt,k)
# decrypt(cipher,k)

