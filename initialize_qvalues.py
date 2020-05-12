import json
from itertools import chain

# Script to create Q-Value JSON file, initilazing with zeros

qval = {}
count = 0
# X -> [0,..400] (diskretizacija na )
# Y -> [-300, -290 ... 160] U [180, 240 ... 420]
for x in range(0, 400):
    for y in range(0, 200):
        # [up, down, right, left, upright, upleft, downright, downleft]
        qval[str(x) + "_" + str(y)] = [0,0,0,0,0,0,0]
        count += 1

print(count)
fd = open("qvalues.json", "w")
json.dump(qval, fd)
fd.close()
