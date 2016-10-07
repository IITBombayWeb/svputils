#!/usr/bin/env python

# creates a filename using various fields in a CSV
# strips filename of common words and special characters


import csv
import sys
import os
import re
import urllib2
import shutil

import hashlib

def hash_a_file(filename):
    
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()

    try:
        with open(filename, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)

        fhash = hasher.hexdigest()
    except EnvironmentError:
        # parent of IOError, OSError *and* WindowsError where available
       fhash = 'Error' 
        
    print(fhash)

    return fhash



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
# 10 Creator                             # 10 File type         
# 11 Date.Created                        # 11 Content Type      
# 12 Coverage.Temporal                   # 12 Format            
# 13 Coverage.Spatial                    # 13 Copyright         
# 14 Publisher                           # 14 Keyword/ Subject  
# 15 Description        
# 16 Language           
# 17 File type          
# 18 Content Type       
# 19 Format             
# 20 Copyright          
# 21 Keyword/ Subject   

def hashedfile(row):
    # replace % characters in URL eg %20 by space
    urlpath = urllib2.unquote(row[3])
    urlprefix = "http://10.129.50.5/nvli/data/"
    
    # Strip urlprefix to find the relative path in local partition
    srcfile = re.sub(urlprefix,'',urlpath)
    
    # the local partition
    srcdir = "/NFSMount/SV-Patel_Data/nvli"
    srcpath = '/'.join([srcdir,srcfile])

    # destroot = "/NFSMount/sardar/files"
    # destpath = '/'.join([destroot, relpath])
    # dirname = os.path.dirname(destpath)
    # if not os.path.exists(dirname):
    #     os.makedirs(dirname)
    
    #os.rename is a mv and needs permissions to delete srcpath
    print 'Hashing from %s ' % srcpath
    sys.stdout.flush()

    filehash = hash_a_file(srcpath)

    hrow = []

    if (filehash != 'Error'):
        hrow = row
        hrow.insert(22,filehash)

    return hrow


###############################  Main Script ###############################

if (len(sys.argv) != 2):
  print "Provide input file to process"
  print sys.argv[0] + " filename.csv\n"
  sys.exit(0)


inpfilename=sys.argv[1]
outfilename="hashed-" + inpfilename


with open(inpfilename,'r') as inpf, open(outfilename,'wb') as outf:

    inpreader  = csv.reader(inpf, delimiter=',')
    hashwriter = csv.writer(outf, delimiter=',')

    header = next(inpreader,None);
    #for i in range(len(header)):
    #    print i, header[i]
    outheader = header
    hashwriter.writerow(outheader)

    
    nrows = 0
    for irow in inpreader:
        result = hashedfile(irow)
        if result:
            hashwriter.writerow(result)
            nrows += 1

print
print '===================================================='
print 'Processed', nrows, "rows"
print 'Use', outfilename, "to sort and remove duplicates"
print

    
        
