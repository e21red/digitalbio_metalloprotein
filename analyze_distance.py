#!/usr/bin/env python
from matplotlib import use
use('Agg')
import matplotlib.pyplot as plt

import math, sys
from collections import defaultdict, Counter

g = open("./metals.txt")
METALS = [line.strip("\n") for line in g.readlines()] #["CHL", "SF4", "HEM", "NA", "FE", "ZN", "MG", "MN", "CU", "NI", "ER", "MB", "K", "CO", "CA"]
g.close()
GROUPS = ["CHL", "SF4", "HEM"]

def slurp_wrappa(filename):
    f = open(filename)
    rettups = []
    for line in f.readlines():
        if line [0:2] == "HB" and line[23] == 'A':
            atom = line[12:16].strip()
 #           if atom not in ["O", "CB", "C", "N"]:
#                print atom
            if atom in METALS:
                seq_no = line[25:29].strip()
                res_seq = line[49:52].strip()
                if res_seq == "":
                    res_seq = line[74:77].strip()
                rettups.append((atom, seq_no))
    return rettups

def find_atoms(filename, metal_tuples):
    f = open(filename)
    hetatms = []
    for line in f.readlines():
        title = line[0:6].strip()
        if title  == 'HETATM' and line[12:16].strip() in (METALS+GROUPS):
            x = float(line[30:38].strip())
            y = float(line[38:46].strip())
            z = float(line[46:54].strip())
            hetatms.append((x,y,z))
    f.close()

    f = open(filename)
    alphas = []
    for line in f.readlines():
        line_type = line[0:6].strip()        
        atom_name = line[12:16].strip()
        if atom_name == "CA" and line_type == "ATOM":
            res_id = line[23:27].strip()
            x = float(line[30:38].strip())
            y = float(line[38:46].strip())
            z = float(line[46:54].strip())
            alphas.append((x,y,z))
    f.close()

    # Counts in case a cofactor serves multiple desolvation spheres
    counts = defaultdict(int)
    for tuple in metal_tuples:
        counts[int(tuple[1])] += 1
    ks = map(int, counts.keys())
    valid_atoms = [tuple[0] for tuple in metal_tuples]

    retarr = []
    f = open(filename)
    lines = [line for line in f.readlines() if line != "\r\n"]

    for line in lines:
        line_type = line[0:6].strip()
        if line_type == 'HETATM' and line[21] in ["", "A"]:
            atom_name = line[12:16].strip()
            if atom_name in valid_atoms:
                cof_id = int(line[22:26].strip())
                if cof_id in ks:
                    x = float(line[30:38].strip())
                    y = float(line[38:46].strip())
                    z = float(line[46:54].strip())
                    dists = sorted([math.sqrt((x-alpha[0])**2 + (y-alpha[1])**2 + (z-alpha[2])**2) for alpha in alphas])

                    for i in range(counts[cof_id]):
                        dist = dists.pop(0)
                        retarr.append((tuple[0], dist))
                    counts[cof_id] = 0 # So that we don't double up
    f.close()
    # returns a list of metal objects
    return retarr

def stddev(lst, avg):
    return math.sqrt(sum(map(lambda x:(x-avg)**2, lst))/len(lst))

def distance_graph(defdict):
    xs = []
    ys = []
    retarr = []
    for cofactor in defdict.keys():
        distances = defdict[cofactor]
        avg = sum(distances)/len(distances)
        retarr.append((cofactor, avg, stddev(distances, avg)))
        for dist in distances:
            xs.append(METALS.index(cofactor))
            ys.append(dist)
        """ Trying to align simple xs, ys. The problem is that we need access to METALS to correctly link with x axis labels """
    plt.title("Metal cofactor distance from desolvation alpha carbon")
    plt.ylabel("Distance in Angstroms")
    plt.xticks(range(len(METALS)), METALS, size="small", rotation=75)
    plt.xlim(-1, len(METALS))
    plt.ylim(0,12)
    plt.plot(xs, ys, 'o')
    plt.savefig("distances.png", dpi=100)
    return retarr
    
def main(args):
    # Setup
    totals = defaultdict(list)
    file_results = defaultdict(list)
    filenames = map(lambda s: (s.split('.')[0]).split('/')[-1], args)
    print filenames
    # Loop through wrappa file, find metals, seq nos
    # Loop through hpdb file, find distance from seq_no-metal to center 


    for filename in filenames:
        wrappa_tuples = []
        w_path = "wrappa_files/"+filename+".w" 
        wrappa_tuples = slurp_wrappa(w_path) # STRUCTURED: (ATOM, SEQUENCE NUMBER, RESIDUE'S SEQUENCE NUMBER)
#            print "W GIVES", wrappa_tuples
        
        if wrappa_tuples != []:
            a_path = "Hpdbs/"+filename+".pdb"
            file_results = find_atoms(a_path, wrappa_tuples)
            if file_results:
                #                    print "THEN NEXT WE GET",  file_results
                for result in file_results:
                    totals[result[0]].append(result[1])
            else:
                print "Metals found, but not corresponding atoms, in file", filename
        else:
            print "No metals found in file", filename

    values = distance_graph(totals)
    for value in values:
        print "%s: Average Distance from CA = %.2f \AA, Standard Deviation = %.2f \AA" %(value[0], value[1], value[2])

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
