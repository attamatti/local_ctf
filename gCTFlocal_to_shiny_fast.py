#!/usr/bin/python
##############################################
### FETCH COPY - (fbsmi2017-03-03 09:19:22.233174) - download a fresh copy if necessary
##############################################

# generalized script for messing with starfiles


import sys
import re

if len(sys.argv) < 4:
    sys.exit('USAGE: gCTFlocal_to_shiny.py <original file> <shiny file> <output file>\nrun with --stats flag to get statistics... (requires numpy)')
    
#------- function test if string is a number --------------------------#
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
#-----------------------------------------------------------------------

###---------function: read the star file get the header, labels, and data -------------#######
def read_starfile(f,d):
    alldata = open(f,'r').readlines()
    labelsdic = {}
    data = []
    header = []
    for i in alldata:
        if '#' in i:
            labelsdic[i.split('#')[0]] = int(i.split('#')[1])-1
        if len(i.split()) > 3:
            data.append(i.split())
        if len(i.split()) < 3:
            header.append(i.strip("\n"))
    if d == True:
        return(labelsdic,header,data)
    else:
        return(labelsdic)
#---------------------------------------------------------------------------------------------#

#------ function: write all of the numbers in the fortran format ---------------------------#
def make_pretty_numbers(dataarray):
    prettyarray = []
    for line in dataarray:
        linestr = ""
        for i in line:
            if is_number(i):
                count = len(i.split('.'))
                if count > 1:
                    i = float(i)
                    if len(str(i).split('.')[0]) > 5:
                        linestr= linestr+"{0:.6e} ".format(i)
                    else:
                        linestr= linestr+"{0:12.6f} ".format(i)
                else:
                    linestr= linestr+"{0: 12d} ".format(int(i))
            else:
                linestr= linestr+"{0} ".format(i)
        prettyarray.append(linestr)
    return prettyarray
#---------------------------------------------------------------------------------------------#

original = sys.argv[1]
shiny = sys.argv[2]
(slabels,sheader,sdata) = read_starfile(shiny,True)
(olabels,oheader,odata) = read_starfile(original,True)

counter = 0
newdata = []
ppctfs = {}
for i in odata:
    newDFV = i[olabels['_rlnDefocusV ']]
    newDFU = i[olabels['_rlnDefocusU ']]
    newDFA = i[olabels['_rlnDefocusAngle ']]
    name  = i[olabels['_rlnImageName ']]
    ppctfs[name] =(newDFV,newDFU,newDFA)
for i in sdata:
    name = i[slabels['_rlnOriginalParticleName ']]
    i[slabels['_rlnDefocusV ']] = ppctfs[name][0]
    i[slabels['_rlnDefocusU ']] = ppctfs[name][1]
    i[slabels['_rlnDefocusAngle ']] = ppctfs[name][2]
    newdata.append(i)
    #print '*',i
    counter +=1
    if counter == 1000:
        sys.stdout.write('.')
        sys.stdout.flush()
        counter = 0

output = open(sys.argv[3],'w')
prettydata = make_pretty_numbers(newdata)
for i in sheader:
    output.write('{0}\n'.format(i))
for i in prettydata:
    output.write('{0}\n'.format(i))