# This script is used to transform data: plaintxt dictionary
# and word dictionary to datastructures (C arrays) to be
# embedded in the Cpp code

import os
from os import error

c2id = {' ':0,'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,'j':10,'k':11,'l':12,'m':13,'n':14,'o':15,'p':16,'q':17,'r':18,'s':19,'t':20,'u':21,'v':22,'w':23,'x':24,'y':25, 'z':26}

def marshall_words(wfile = "word.txt"):
    wpath = wfile
    if not os.path.exists(wpath):
        wpath = f"../{wfile}"
    
    if not os.path.exists(wpath):
        wpath = f"./data/{wfile}"

    if not os.path.exists(wpath):
        raise error("FILE NOT FOUND")

    with open(wpath,"r") as fp:
        words = [x[:-1] for x in fp.readlines()]
        kernel = ""
        wlens = []
        for wi,w in enumerate(words):
            wd = ""
            wlens.append(str(len(w)))
            for cx,c in enumerate(w):
                wd += str(c2id[c])
                if cx+1<len(w):
                    wd += ","
            wd = f"{{{wd}}}"
            kernel += wd
            if wi+1 < len(words):
                kernel += ","
        kernel = f"constexpr aindex_t words[WORD_DICT_SIZE][MAX_WORD_LEN] = {{{kernel}}};"
        print(kernel)
        wlens = ",".join(wlens)
        wlens = f"constexpr int wlens[WORD_DICT_SIZE] = {{{wlens}}};"
        print(wlens)

def marshall_ptxts(wfile = "plaintxts.txt"):
    wpath = wfile
    if not os.path.exists(wpath):
        wpath = f"../{wfile}"
    
    if not os.path.exists(wpath):
        wpath = f"./data/{wfile}"

    if not os.path.exists(wpath):
        raise error("FILE NOT FOUND")

    with open(wpath,"r") as fp:
        words = [x[:-1] for x in fp.readlines()]
        kernel = ""

        for wi,w in enumerate(words):
            wd = ""

            for cx,c in enumerate(w):
                wd += str(c2id[c])
                if cx+1<len(w):
                    wd += ","
            wd = f"{{{wd}}}"
            kernel += wd
            if wi+1 < len(words):
                kernel += ","
        kernel = f"constexpr aindex_t plaintxts[PLAINTXT_DICT_SIZE][TXT_LEN] = {{{kernel}}};"
        print(kernel)


if __name__=="__main__":
    marshall_words()
