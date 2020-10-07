from os import stat


c2id = {' ':0,'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,'j':10,'k':11,'l':12,'m':13,'n':14,'o':15,'p':16,'q':17,'r':18,'s':19,'t':20,'u':21,'v':22,'w':23,'x':24,'y':25, 'z':26}
alphabet = " abcdefghijklmnopqrstuvwxyz"
T = 106 # Sum(rowlen)
rowlen = [19,7,1,2,4,10,2,2,5,6,1,1,3,2,6,6,2,1,5,5,7,2,1,2,1,2,1]
rowlen_d = dict()
for i,rl in enumerate(rowlen):
    rowlen_d[alphabet[i]] = rl

words = [x.strip() for x in open("./data/word.txt").readlines()]
ptxt_dict = [x for x in open("./data/plaintxts.txt").readlines()]

def checker(cipher,ptxt):
    # print(ptxt)
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
                # print(f"NOT SAME! CAUGHT AT {i}")
                return -1
        if len(k[pc])>rowlen_d[pc]:
            # print(f"NOT SAME! CAUGHT AT {i}")
            return -1
    return 1

cipher = [int(x) for x in input().split(",")]
# print(cipher)

def gen_empty_key():
    k = dict()
    for i in range(27):
        k[i] = set()
    return k

class State:
    def __init__(self):
        self.ptxt = []
        for i in range(500):
            self.ptxt.append(0)
        self.wstate = []
        for i in range(500):
            self.wstate.append(0)
        self.wslen = 0
        self.plen = 0
        self.hits = []
        for i in range(T):
            self.hits.append(0)
        self.tbl = gen_empty_key()
        self.seen = dict()

    def consume(self,plc):
        cv = cipher[self.plen]
        if(self.hits[cv]>0):
            pe = self.seen[cv]
            if pe!= plc:
                return False
            else:
                self.hits[cv] += 1
                self.ptxt[self.plen] = pe
                self.plen += 1
                return True
        else:
            if len(self.tbl[plc])+1>rowlen[plc]:
                return False
            else:
                self.seen[cv] = plc
                self.tbl[plc].add(cv)
                self.hits[cv] += 1
                self.ptxt[self.plen] = plc
                self.plen += 1
                return True

    def rollback(self,num):
        # print(self.tbl)
        # print(self.seen)
        for i in range(num):
            cv = cipher[self.plen -i - 1]
            pv = self.ptxt[self.plen -i - 1]
            self.hits[cv] = self.hits[cv] - 1
            if self.hits[cv] == 0:
                self.tbl[pv].remove(cv)
                self.seen.pop(cv)
        self.plen -= num

    def advance(self):
        works = False
        found = 0
        wdi = self.wstate[self.wslen]
        
        # xxd = ""
        # for i in range(self.wslen):
        #     xxd += f"{words[self.wstate[i]]} "
        #     # print(f"{words[self.wstate[i]]} ",end="")
        # # print("\n")
        # if xxd.startswith("dislocating"):
        #     breakpoint()

        while (not works) and (wdi<len(words)):
            works = True
            for ci in range(len(words[wdi])+1):
                ch = 0
                if ci<len(words[wdi]):
                    ch = c2id[words[wdi][ci]]
                cons = self.consume(ch)
                if not cons:
                    works = False
                    self.rollback(ci)
                    break
                else:
                    if self.plen == 500:
                        found = 1
                        return 1
            
            if works:
                break
            else:
                wdi+=1
        
        if works:
            self.wstate[self.wslen] = wdi
            self.wslen += 1
            return 0

        else:
            wwdi = self.wstate[self.wslen-1]
            self.wstate[self.wslen] = 0
            while wwdi> (len(words)-2):
                self.rollback(len(words[self.wstate[self.wslen-1]])+1)
                self.wstate[self.wslen-1] = 0
                self.wslen -= 1
                if self.wslen < 1:
                    return -1
                wwdi = self.wstate[self.wslen-1]
            self.rollback(len(words[self.wstate[self.wslen-1]])+1)
            self.wstate[self.wslen - 1] += 1
            self.wslen -= 1
            return self.advance()


def decrypt():
    state = State()
    found = 0
    while found==0:
        found = state.advance()
    # print(found)
    for i,pc in enumerate(state.ptxt):
        print(alphabet[pc],end="")
    print("\n")

import time
t0 = time.time_ns()
for p in ptxt_dict:
    if checker(cipher,p)!=-1:
        print(p)
        exit(0)
decrypt()
print(time.time_ns()-t0)