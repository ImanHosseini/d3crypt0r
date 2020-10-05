import time, subprocess, os

dnull = open(os.devnull,'w')

dnames = os.listdir("./decry") 
dexes = [f"./decry/{x}/Decry.exe" for x in dnames]

ciphers = [f"./tests/ciphers/{x}" for x in os.listdir("./tests/ciphers/")]
# print(ciphers)

dtimes = dict()

for di,dexe in enumerate(dexes):
    dtimes[dnames[di]] = []
    for ciph in ciphers:
        t0 = time.time_ns()
        proc = subprocess.Popen([dexe],stdin=subprocess.PIPE,stdout=dnull)    
        dt = time.time_ns()-t0
        dtimes[dnames[di]].append(dt)

import json
outfile = open("stats.txt","w").write(json.dumps(dtimes)) 

# t0 = time.time_ns()
# proc = subprocess.Popen(['./decry/win64_msvc/Decry.exe'],stdin=subprocess.PIPE,stdout=dnull)
# ciph = open("./tests/ciphers/c_0_0.txt","r").readline()
# proc.stdin.write(ciph.encode('ascii')+b"\n")
# proc.stdin.flush()
# proc.wait()
# print(time.time_ns()-t0)

# t0 = time.time_ns()
# proc = subprocess.Popen(['./decry/win64_msvc/Decry.exe','-t','16'],stdin=subprocess.PIPE,stdout=dnull)
# ciph = open("./tests/ciphers/c_0_0.txt","r").readline()
# proc.stdin.write(ciph.encode('ascii')+b"\n")
# proc.stdin.flush()
# proc.wait()
# print(time.time_ns()-t0)