#!/usr/bin/env python

import math, sys

def read(filename):
    f = open(filename)
    metals = []
    for line in f.readlines():
        if line[0:6].strip() in ["ATOM", "HETATM"]:
            name = line[12:16].strip()
            id = line[22:26].strip()
            x = line[30:38].strip()
            y = line[38:46].strip()
            z = line[46:54].strip()
            metals.append(name, id, (x,y,z))
    return metals

class Metal:
    def __init__(self, name, id, location):
        self.name = name  # Also used for type info
        self.location = location
        self.id = id
    
    def distance(self, point):
        x,y,z = self.location
        px,py,pz = point
        return math.sqrt((x-px)**2, (y-py)**2, (z-pz)**2)

    
