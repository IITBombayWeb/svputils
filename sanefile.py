#!/usr/bin/env python

#parse the results file and vaidate entries


import csv
import sys
import re


def sanefilename(strlist):
    filename = '-'.join(strlist)

# Input header                           # output header        
# 0 Assignee                             # 0  Unique ID (in local context)
# 1 Status                               # 1  Filename (relative)
# 2 Comment/Remark                       # 2  Title              
# 3 Local URL                            # 3  Creator           
# 4 YYYY                                 # 4  Date              
# 5 Source ID                            # 5  Coverage.Temporal 
# 6 Accession Number                     # 6  Coverage.Spatial  
# 7 Internal ID / Seq ID                 # 7  Publisher         
# 8 Unique Resource ID                   # 8  Description       
# 9 Title                                # 9  Language          
# 10 Renamed File                        # 10 File type         
# 11  Sane file                          # 11 Content Type      
# 12 Creator                             # 12 Format            
# 13 Date.Created                        # 13 Copyright         
# 14 Coverage.Temporal                   # 14 Keyword/ Subject  
# 15 Coverage.Spatial
# 16 Publisher
# 17 Description
# 18 Language
# 19 File type
# 20 Content Type
# 21 Format
# 22 Copyright
# 23 Keyword/ Subject

def makesane(row):
    filename = sanefilename([row[8], row[9] + '.' + row[19]])
    sane = [ row[8], 
    
    return sane


###############################  Main Script ###############################

if (len(sys.argv) != 2):
  print "Provide input file to process"
  print sys.argv[0] + " filename.csv\n"
  sys.exit(0)


inpfilename=sys.argv[1]
outfilename="processed.csv"

















with open(inpfilename,'r') as inpf, open(outfilename,'wb') as outf:

    inpreader  = csv.reader(inpf, delimiter=',')
    sanewriter = csv.writer(outf, delimiter=',')

    header = next(inpreader,None);
    for i in range(len(header)):
        print i, header[i]

    nrows = 0
    for irow in inpreader:
        nrows += 1
        result = makesane(irow)
        sanewriter.writerow(result)


print 'Processed', len(irow), "rows"

    
        
