#!/usr/bin/env python
from matplotlib import use
use('Agg')
import matplotlib.pyplot as plt

import math, sys
from collections import defaultdict, Counter

# FUCK ALPHA CARBONS NOBODY LIKES THEM -- Also, using hard coded ids here
METALS = ["CHL", "SF4", "HEM", "NA", "FE", "ZN", "MG", "MN", "CU", "NI", "ER", "MB", "K", "CO", "CA"]
#COLORS = dict(zip(METALS, ["#%x" %111111*i for i in range(15)] ))

class Metal:
    def __init__(self, name, id, amn):
        self.name = name  # Also used for type info
        self.amino_acid = amn
        self.id = id
'''    
    def distance(self, point):
        x,y,z = self.location
        px,py,pz = point
        return math.sqrt((x-px)**2, (y-py)**2, (z-pz)**2)
'''

def slurp(filename):
    f = open(filename)
    metals = []
    for line in f.readlines():
        if line[0:2] == "HB":
            name = line[12:16].strip()
            seq = line[23]
            if name in METALS and seq in ["", "A"]:
                id = line[26:30].strip()
                amn = line[42:45].strip()
                if amn == "":
                    amn = line[65:68].strip()
                #                x = line[30:38].strip()
                #                y = line[38:46].strip()
                #                z = line[46:54].strip()
                    metals.append(Metal(name, id, amn))
    # returns a list of metal objects
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

def group_by_amino(metals):
    metal_list = []
    amino_list = []

    amino_counts = defaultdict(list)
    metal_counts = defaultdict(list)
    for metal in metals:
        metal_counts[metal.name].append(metal.amino_acid)
        amino_counts[metal.amino_acid].append(metal.name)
    metal_counter = Counter(metal_counts)
    amino_counter = Counter(amino_counts)
    for metal_code in metal_counts:
        counter = Counter(metal_counts[metal_code])
        metal_list.append((metal_code, zip(counter.keys(), counter.values())))
    for amino_code in amino_counts:
        counter = Counter(amino_counts[amino_code])
        amino_list.append((amino_code, zip(counter.keys(), counter.values())))

    # Each list is a tuple (ID, [(sub_id, count), (sub_id, count), ...]
    return metal_list, amino_list

def sphere_graph(metals):
    flat_metals = [tuple for sublist in metals for tuple in sublist]
    xs = []
    ys = []# dict( zip(METALS, [0]*len(METALS)) )
    """ Trying to align simple xs, ys. The problem is that we need access to METALS to correctly link with x axis labels """
    colors = []
    plt.xticks(range(len(METALS)), METALS, size="small")
    plt.xlim(-1, len(METALS))
    plt.ylim(0,10)
    for tuple in flat_metals:
        for xys in tuple[1]:
            xs.append(METALS.index(tuple[0]))
            ys.append(xys[1])
            colors.append(tuple[0])
#    print xs, ys
    plt.plot(xs, ys, 'o')
    plt.savefig("desolv.png")
    
def main(args):
    grouped_metals = []
    amn_metals = []
    for filename in args:
        metals = slurp(filename)
        if metals:
            grouped_metals.append(compile_counts(metals))
            amn_metals += metals
    sphere_graph(grouped_metals)

    metal_list, amino_list = group_by_amino(amn_metals)
    for lst in [metal_list, amino_list]:
        for key, pairs in lst:
            for pair in pairs:
                print "%s: %s, %d" %(key, pair[0], pair[1])
        print "-------------------"

if __name__ == '__main__':
    sys.exit(main(sys.argv))
