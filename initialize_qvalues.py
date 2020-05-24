import json
from itertools import chain

# Script to create Q-Value JSON file, initilazing with zeros

qval = {}
count = 0
# X -> [0,..400] 
# Y -> [0,..200]
for x in range(0, 400): #vodoravna diskretizacija
    for y in range(0, 200): #vertikalna diskretizacija
        for vel in range(0, 20): #diskretizacija hitrosti
            # [up, down, right, left, upright, upleft, downright, downleft]
            qval[str(x) + "_" + str(y) + "_" + str(vel)] = [0,0,0,0,0,0,0]
            count += 1

print(count)
fd = open("qvalues.json", "w")
json.dump(qval, fd)
fd.close()
