import os, subprocess

#Batch Hydrogen Adder-Using Command line Mol Probity (Reduce)
#Oluwaseun Ogedengbe
#A simple script to add Hs to pdb files and save the results
#Instructions:
#modify the instruction variable accordingly for the desired argument.
#place the bhadder.py file into the same directory as reduce.exe
#place all pdbs to be converted in the same directory as reduce.exe
#run bhadder.py

job = []
for files in os.listdir("."):
    if files.endswith(".pdb"):
        print files
        job.append(files)

try: os.makedirs('hpdbs')
except OSError: pass

instruction = 'reduce -NOFLIP '
print 'performing '+instruction
for pdb in job:
    fh = open('hpdbs/'+pdb,'w')
    p = subprocess.Popen(instruction + pdb, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        fh.write(line)
        fh.write('\n')
    retval = p.wait()
    fh.close()

print 'Hydrogens added sucessfully'
