import os, subprocess, sys

#Batch Hydrogen Adder-Using Command line Mol Probity (Reduce)
#Oluwaseun Ogedengbe
#A simple script to add Hs to pdb files and save the results
#Instructions:
#modify the instruction variable accordingly for the desired argument.
#place the bhadder.py file into the same directory as reduce.exe
#place all pdbs to be converted in the same directory as reduce.exe
#run bhadder.py

job = []
for arg in sys.argv[1:]:
    if arg[-3:] != "txt":
        for files in os.listdir("./"+arg):
            if files.endswith(".pdb"):
                print files
                job.append(files)

try: os.makedirs('hpdbs')
except OSError: pass

instruction = '../reduce -BUILD '
print 'performing '+instruction
for pdb in job:
    fh = open('hpdbs/'+pdb,'w')
    cmd = instruction + pdb
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in p.stdout.readlines():
        fh.write(line)
        fh.write('\n')
    retval = p.wait()
    fh.close()

print 'Hydrogens added sucessfully'
