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



allowedfmt = [ 'jpg', 'jpeg', 'wav', 'png', 'gif',
               'mp4', 'mpg', 'mpeg', 'wmv',
               'pdf', 'mp3', 'wav'] 



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
       print 'Error, not found: %s' % filename
       
        
    #print(fhash)

    return fhash



# Input header                           
# 0 Assignee                             
# 1 Status                                
# 2 Comment/Remark                         
# 3 Local URL                             
# 4 YYYY                                  
# 5 Source ID                             
# 6 Accession Number                      
# 7 Internal ID / Seq ID                  
# 8 Unique Resource ID                    
# 9 Title                                 
# 10 Creator                              
# 11 Date.Created                         
# 12 Coverage.Temporal                    
# 13 Coverage.Spatial                     
# 14 Publisher                            
# 15 Description        
# 16 Language           
# 17 File type          
# 18 Content Type       
# 19 Format             
# 20 Copyright          
# 21 Keyword/ Subject   
# 22 File hash

def hashedfile(row):

    global allowedfmt
    
    # replace % characters in URL eg %20 by space
    urlpath = urllib2.unquote(row[3])
    urlprefix = "http://10.129.50.5/nvli/data/"
    
    # Strip urlprefix to find the relative path in local partition
    srcfile = re.sub(urlprefix,'',urlpath)
    
    # the local partition
    srcdir = "/NFSMount/SV-Patel_Data/nvli"
    srcpath = '/'.join([srcdir,srcfile])


    fmt = row[19].lower()

    hrow = []

    if fmt not in allowedfmt:
        print 'Warning, format not imported: %s for %s' % (fmt,srcpath)
        return hrow
    
    print 'Hashing %s ' % srcpath
    sys.stdout.flush()

    filehash = hash_a_file(srcpath)


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

    outheader.insert(22,"File hash")
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

    
        
