# This script requrie python >= 3.8

import math
rowlen = [19,7,1,2,4,10,2,2,5,6,1,1,3,2,6,6,2,1,5,5,7,2,1,2,1,2,1]
sumrowlen = 106

# sumrowlen -= 50
# rowlen = [1,2,2,2,1,1,1,3,2,6,6,2,1,5,5,7,2,1,2,1,2,1]

sumrowlen = 12
rowlen = [2,10]

val = 1
for x in rowlen:
    val = val*math.comb(sumrowlen,x)
    sumrowlen -= x

print(val)