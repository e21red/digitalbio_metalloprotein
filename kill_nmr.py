#!/usr/bin/env python

import sys

seq_pos = {"ATOM":21, "ANISOU":21, "HETATM":21, "HELIX":19, "SHEET":19, 
           "SEQRES":11, "DBREF":12, "SEQADV":16}

for i, filename in enumerate(sys.argv):
    if i != 0:
        f = open(filename)
        filename = filename[0:-4]
        g = open("%s_revised.pdb" %(filename), 'w')
        for line in f.readlines():
            line_title = line.split()[0]
            if line_title in seq_pos.keys():
                print line_title, line[seq_pos[line_title]]
                if line[seq_pos[line_title]] in ["", "A"]:
                    g.write(line)
            else:
                g.write(line)
        f.close()
        g.close()
