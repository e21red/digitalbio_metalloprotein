#!/usr/bin/env python

import math, sys
from collections import defaultdict, Counter

# FUCK ALPHA CARBONS NOBODY LIKES THEM
METALS = ["NA", "FE", "ZN", "MG", "MN", "CU", "NI", "ER", "MB", "K", "CO"] #, "CA"]

def slurp(filename):
    f = open(filename)
    metals = []
    for line in f.readlines():
        if line[0:2] == "HB":
            name = line[12:16].strip()
            seq = line[23]
            if name in METALS and seq in ["", "A"]:
                id = line[26:30].strip()
                #                x = line[30:38].strip()
                #                y = line[38:46].strip()
                #                z = line[46:54].strip()
                metals.append(Metal(name, id, (0,0,0)))
    return metals

def compile_counts(metals):
    retlist = []
    file_metals = defaultdict(list)
    for metal in metals:
        file_metals[metal.name].append(metal.id)
    for metal_code in file_metals:
        id_list = map(int, file_metals[metal_code])
        counter = Counter(id_list)
        retlist.append((metal_code, zip(counter.keys(), counter.values())))
    return retlist
    
class Metal:
    def __init__(self, name, id, location):
        self.name = name  # Also used for type info
        self.location = location
        self.id = id
    
    def distance(self, point):
        x,y,z = self.location
        px,py,pz = point
        return math.sqrt((x-px)**2, (y-py)**2, (z-pz)**2)

    
def main(args):
    all_metals = []
    for filename in args:
        metals = slurp(filename)
        if metals:
            all_metals.append(compile_counts(metals))
    print all_metals
    


if __name__ == '__main__':
    sys.exit(main(sys.argv))
