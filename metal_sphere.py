#!/usr/bin/env python
from matplotlib import use
use('Agg')
import matplotlib.pyplot as plt

import math, sys
from collections import defaultdict, Counter

g = open("./metals.txt")
METALS = [line.strip("\n") for line in g.readlines()] #["CHL", "SF4", "HEM", "NA", "FE", "ZN", "MG", "MN", "CU", "NI", "ER", "MB", "K", "CO", "CA"]
g.close()

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

def adjust_total_counts(filename, counts):
    f = open(filename)
    for line in f.readlines():
        if line == "END":
            print "HELLO"
        if line[0:6] == "HETATM":
            name = line[12:16].strip()
            if name in METALS and line[21] in ["A", ""]:
                print name, line[:-2]
                counts[name] += 1
    print filename, counts

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

def stddev(lst, avg):
    return math.sqrt(sum(map(lambda x:(x-avg)**2, lst))/len(lst))

def sphere_graph(metals, total_metal_counts):
    flat_metals = [tuple for sublist in metals for tuple in sublist]
    xs = []
    ys = []
    retarr = []

    uniqs_found = defaultdict(int)
    for ion, association in flat_metals:
        uniqs_found[ion] += len(association)

    served = defaultdict(list)
    for metal, x in flat_metals:
        served[metal].extend([pair[1] for pair in x])

    for cofactor in served.keys():
        lst = served[cofactor]
        avg = sum(lst)/float(len(lst))
        retarr.append((cofactor, avg, stddev(lst, avg)))

        print cofactor, uniqs_found[cofactor], total_metal_counts[cofactor]
        if uniqs_found[cofactor] != total_metal_counts[cofactor]:
            for i in range(total_metal_counts[cofactor] - uniqs_found[cofactor]):
                xs.append(METALS.index(cofactor))
                ys.append(0)

    """ Trying to align simple xs, ys. The problem is that we need access to METALS to correctly link with x axis labels """
    colors = []
    plt.xticks(range(len(METALS)), METALS, size="small", rotation=75)
    plt.xlim(-1, len(METALS))
    plt.ylim(0,10)
    plt.ylabel("Desolvation spheres served by atom")
    plt.title("Desolvation spheres served by individual ions")
    for tuple in flat_metals:
        for xys in tuple[1]:
            xs.append(METALS.index(tuple[0]))
            ys.append(xys[1])
            colors.append(tuple[0])

    plt.plot(xs, ys, 'o')
    plt.savefig("desolv.png")


    return retarr
    

def main(args):
    file_results = defaultdict(list)
    filenames = map(lambda s: (s.split('.')[0]).split('/')[-1], args)

    grouped_metals = []
    amn_metals = []
    total_metal_counts = defaultdict(int)
    for filename in filenames:
        metals = slurp("wrappa_files/"+filename+".w")
        adjust_total_counts("Hpdbs/"+filename+".pdb", total_metal_counts)
        if metals:
            grouped_metals.append(compile_counts(metals))
            amn_metals += metals
    values = sphere_graph(grouped_metals, total_metal_counts)
    for value in values:
        print "%s: Average Served Domains = %.2f \AA, Standard Deviation = %.2f \AA" %(value[0], value[1], value[2])

"""
    metal_list, amino_list = group_by_amino(amn_metals)
    for lst in [metal_list, amino_list]:
        for key, pairs in lst:
            for pair in pairs:
                print "%s: %s, %d" %(key, pair[0], pair[1])
        print "-------------------"
"""
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
