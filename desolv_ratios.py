#!/usr/bin/env python
from matplotlib import use
use('Agg')
import re
import matplotlib.pyplot as plt

import math, sys
from collections import defaultdict, Counter

g = open("./metals.txt")
METALS = [line.strip("\n") for line in g.readlines()] #["CHL", "SF4", "HEM", "NA", "FE", "ZN", "MG", "MN", "CU", "NI", "ER", "MB", "K", "CO", "CA"]
g.close()

def truncate_atom(oldname, type):
    if oldname[0] == 'B':
        print oldname
    if oldname == 'BRB':
        name = 'BR'
    name = oldname.translate(None, '0123456789')
    if name not in METALS+['AS','CL','BR'] or type == 'ATOM':
        name = name[0]
    return name

def slurp(filename):
    data = defaultdict(set)
    f = open(filename)
    for line in f.readlines():
        if line[0:2] == "HB":
            C = line[23]
            if C in ["", "A"]:
                id = line[25:30].strip()
                name = truncate_atom(line[12:16].strip(), line[0:6].strip())
                if re.match('\d', name):
                    print "Hello", name
                data[name].add(id)
    f.close()
    retsdict = {}
    for k in data:
        retsdict[k] = len(data[k])
    return retsdict

def check_against_hpdb(filename, desolv_set, ratios):
    full_dict = defaultdict(int)

    f = open(filename)
    for line in f.readlines():
        if line[0:6].strip() in ["ATOM", "HETATM"] and line[21] in ['','A']:
            name = truncate_atom(line[12:16].strip(), line[0:6].strip())
            full_dict[name] += 1
    f.close()
    return interleave(desolv_set, full_dict, ratios)

def add_twotuples(a,b):
    x,y = a
    s,t = b
    return (x+s, y+t)

def print_ratios(dict):
    for key in dict.keys():
        ratio = dict[key]
#        print key
#        print key, ratio, float(ratio[0])/ratio[1] 

def interleave(a, b, ratios):
    for atom in a.keys():
        ratios[atom] = add_twotuples(ratios[atom], (a[atom], b[atom]))
    return ratios

def graph(ratios):
    mxs, oxs, mys, oys = [],[],[],[]
    use, use2 = [], []
    for key in ratios.keys():
        if key not in use:
            if use in METALS:
                use.append(key)
            else:
                use2.append(key)
    base = sorted(use + use2)
    for key in ratios.keys():
        x,y = ratios[key]
        if y != 0:
            value = float(x)/y
            if value > 1:
                value = 1
            if key in METALS:
                mxs.append(base.index(key))
                mys.append(value)
            else:
                oxs.append(base.index(key))
                oys.append(value)
    plt.xlim(0,25)
    plt.ylim(0,1.02)
    plt.xticks(range(len(base)),base, size='small', rotation=75)
    plt.title("Dehydron ratios")
    plt.ylabel("Ration of dehydron-serving atoms to total found")
#    plt.legend(('Metals', 'Nonmetals'), loc='upper right')
    plt.scatter(mxs, mys, color='red', marker='s', label='Metals')
    plt.scatter(oxs, oys, color='blue', marker='D', label='nonmetals')



    plt.savefig("ratios.png")

def main(args):
    ratios = defaultdict(lambda:(0,0))
    filenames = map(lambda s: (s.split('.')[0]).split('/')[-1], args)
    for filename in filenames:
        sets = slurp("wrappa_files/"+filename+".w")
        check_against_hpdb("hpdbs/"+filename+".pdb", sets, ratios)
    print_ratios(ratios)
    graph(ratios)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
