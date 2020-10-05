import random

alphabet = " abcdefghijklmnopqrstuvwxyz"
T = 106 # Sum(rowlen)
rowlen = [19,7,1,2,4,10,2,2,5,6,1,1,3,2,6,6,2,1,5,5,7,2,1,2,1,2,1]
rowlen_d = dict()
for i,rl in enumerate(rowlen):
    rowlen_d[alphabet[i]] = rl

def get_words(fname="./data/word.txt"):
    with open("./data/word.txt") as wordsf:
        words = [x.strip().lower() for x in wordsf.readlines()]
        words = list(filter(lambda x: "'" not in x,words))
        return words

def gen_random_plaintxt(fname = "./data/word.txt"):
    L = 500
    ptxt = ""
    words = []
    with open(fname) as wordsf:
        words = [x.strip().lower() for x in wordsf.readlines()]
        words = list(filter(lambda x: "'" not in x,words))
        # print(len(words))
    curs = 0
    # print(len(words))
    while(curs<L):
        filtered_words = list(filter(lambda x: curs+len(x)<=L, words))
        if len(filtered_words) == 0:
            ptxt = ptxt[:-1]
            lw = ptxt.split()[-1]
            ptxt = ptxt[:-len(lw)]
            curs -= (len(w)+1)
            continue
        w = filtered_words[random.randint(0,len(filtered_words)-1)]
        if(curs + len(w) == L):
            ptxt = ptxt + w
            break
        ptxt = ptxt + w +" "
        curs += len(w)+1
    # Kill trailing space
    
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
    ktbl = dict()
    for a in alphabet:
        k[a] = set()
    for i,c in enumerate(cipher):
        pc = ptxt[i]
        k[pc].add(c)
        if c not in ktbl:
            ktbl[c] = pc
        else:
            c_map = ktbl[c]
            if c_map != pc:
                print(f"NOT SAME! CAUGHT AT {i}")
                return
        if len(k[pc])>rowlen_d[pc]:
            print(f"NOT SAME! CAUGHT AT {i}")
            return

def gen_from_pdic():
    k = gen_key()
    ptxt1 = open("./data/plaintxts.txt").readlines()[4]
    ptxt2 = gen_random_plaintxt()
    cipher1 = encrypt(ptxt1,k)
    for x in cipher1:
        print(x,end=",")
    print(f"\n{k}")
    # print(cipher1)
    # cipher2 = encrypt(ptxt2,k)
    # checker(cipher1,ptxt2)

def gen_from_words(k = None, ptxt = None):
    if k is None:
        k = gen_key()
    if ptxt is None:
        ptxt = gen_random_plaintxt()
    ciph = encrypt(ptxt,k)
    ciph_ = ""
    for x in ciph:
        ciph_ += f"{str(x)},"
    
    return ciph_[:-1]
    # print(ptxt)
    # for x in ciph:
    #     print(x,end=",")
    # print(f"\n{k}") 

import json

if __name__=="__main__":
    KNUM = 10 
    MSGNUM = 50
    keyz = [gen_key() for _ in range(KNUM)]
    msgz = [gen_random_plaintxt() for _ in range(MSGNUM)]
    for i,k in enumerate(keyz):
        open(f"./tests/keys/k_{i}.txt","w").write(json.dumps(k))
    for i,m in enumerate(msgz):
        open(f"./tests/msgs/m_{i}.txt","w").write(m)
    for ki,k in enumerate(keyz):
        for mi,m in enumerate(msgz):
            open(f"./tests/ciphers/c_{ki}_{mi}.txt","w").write(gen_from_words(k,m))

# k = gen_key()
# ptxt = gen_random_plaintxt()
# print(ptxt)
# cipher = encrypt(ptxt,k)
# decrypt(cipher,k)

