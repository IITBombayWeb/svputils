#!/usr/bin/env python

#parse the results file and vaidate entries


import csv
import sys
import os
import re
import urllib2
import shutil


def sanefilename(strlist):
    filename = '-'.join(strlist).strip().lower()
    wordlist=[
        "a", "an", "as", "at", "before", "but", "by", "for", "from", "is", "in", "into", "like", "of", "off", "on", "onto", "per", "since", "than", "the", "this", "that", " up", "via", "with"] 

    # \b for begin or end of word, | is logical OR
    # "\ba\b|\ban\b|\bas\b" for a, an as
    prepregex =  r"\b" + r"\b|\b".join(wordlist) + r"\b"
    spaceregex = r"\s"
    hypregex = r"-+"
    splcharegex = r'[\\~!@#$%^&*(){}<>?/|,;:`\[\]+_="\']+'

    filename = re.sub(prepregex,'',filename)
    filename = re.sub(spaceregex,'-',filename)
    filename = re.sub(splcharegex,'',filename)
    filename = re.sub(hypregex,'-',filename)
    return filename

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

def makesane(row):
    # made from uniq ID, title and extension
    filename = sanefilename([row[8], row[9] + '.' + row[19]])

    # source
    dirname = sanefilename([row[5]])

    relpath = dirname + '/' + filename


    urlpath = urllib2.unquote(row[3])
    urlprefix = "http://10.129.50.5/nvli/data/"
    
    srcfile = re.sub(urlprefix,'',urlpath)
    
    srcdir = "/NFSMount/SV-Patel_Data/nvli"
    srcpath = '/'.join([srcdir,srcfile])

    destroot = "/NFSMount/sardar/files"
    destpath = '/'.join([destroot, relpath])
    print srcpath,destpath

    dirname = os.path.dirname(destpath)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    
    shutil.copyfile(srcpath,destpath)


    sane = [row[8],relpath,row[9]] + row[10:]
    #sane = [filename]
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
    #for i in range(len(header)):
    #    print i, header[i]

    nrows = 0
    for irow in inpreader:
        nrows += 1
        result = makesane(irow)
        sanewriter.writerow(result)


print 'Processed', nrows, "rows"

    
        
