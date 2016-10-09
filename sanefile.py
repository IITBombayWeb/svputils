#!/usr/bin/env python

# creates a filename using various fields in a CSV
# strips filename of common words and special characters


import csv
import sys
import os
import re
import urllib2
import shutil


def sanefilename(strlist):
    filename = '-'.join(strlist).strip().lower()
    prunewordlist=[
        "a", "an", "as", "at", "before", "but", "by", "for", "from", "is", "in", "into", "like", "of", "off", "on", "onto", "per", "since", "than", "the", "this", "that", " up", "via", "with"] 

    # \b for begin or end of word, | is logical OR
    # "\ba\b|\ban\b|\bas\b" for a, an as
    prepregex =  r"\b" + r"\b|\b".join(prunewordlist) + r"\b"
    spaceregex = r"\s"
    hypregex = r"-+"
    splcharegex = r'[\\~!@#$%^&*(){}<>?/|,;:`\[\]+_="\']+'

    filename = re.sub(prepregex,'',filename)
    filename = re.sub(spaceregex,'-',filename)
    filename = re.sub(splcharegex,'',filename)
    filename = re.sub(hypregex,'-',filename)
    return filename

# Input header                           # output header        
# 0  Assignee                            # 0  Unique ID (in local context)
# 1  Status                              # 1  Filename (relative)
# 2  Comment/Remark                      # 2  SHA1
# 3  Local URL                           # 3  Title 
# 4  SHA1 Hash                           # 4  Creator           
# 5  YYYY                                # 5  Date              
# 6  Source ID                           # 6  Coverage.Temporal 
# 7  Accession Number                    # 7  Coverage.Spatial  
# 8  Internal ID / Seq ID                # 8  Publisher         
# 9  Unique Resource ID                  # 9  Description       
# 10 Title                               # 10 Language          
# 11 Creator                             # 11 File type         
# 12 Date.Created                        # 12 Content Type      
# 13 Coverage.Temporal                   # 13 Format            
# 14 Coverage.Spatial                    # 14 Copyright         
# 15 Publisher                           # 15 Keyword/ Subject 
# 16 Description           
# 17 Language              
# 18 File type             
# 19 Content Type          
# 20 Format                
# 22 Copyright             
# 21 File hash             
# 22 Keyword/ Subject      

def makesane(row):
    # made from uniq ID, title and extension
    title = row[9].rstrip('.')
    fmt = row[19].lower()
    filename = sanefilename([row[8], title + '.' + fmt])

    # source 
    sourceid = row[6]
    dirname = sanefilename([sourceid])
    # create a subdir for each hyphenated part of uniq ID
    dirname = re.sub(r"-",'/',dirname) 

    relpath = 'archive/' + dirname + '/' + filename


    # replace % characters in URL eg %20 by space
    urlpath = urllib2.unquote(row[3])
    urlprefix = "http://10.129.50.5/nvli/data/"
    
    # Strip urlprefix to find the relative path in local partition
    srcfile = re.sub(urlprefix,'',urlpath)
    
    # the local partition
    srcdir = "/NFSMount/SV-Patel_Data/nvli"
    srcpath = '/'.join([srcdir,srcfile])

    destroot = "/NFSMount/sardar/files"
    destpath = '/'.join([destroot, relpath])

    dirname = os.path.dirname(destpath)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    
    #os.rename is a mv and needs permissions to delete srcpath
    print 'Copying from %s to \n\t%s ' % (srcpath,destpath)
    sys.stdout.flush()

    try: 
        shutil.copyfile(srcpath,destpath)
        sane = [row[8],relpath,row[4]] + row[10:]
    # eg. src and dest are the same file
    except shutil.Error as e:
        print('Error: %s' % e)
        sane = "Error"
    # eg. source or destination doesn't exist
    except IOError as e:
        print('Error: %s, %s' % (srcpath, e.strerror))
        sane = "Error"


    #sane = [filename]
    return sane


###############################  Main Script ###############################

if (len(sys.argv) != 2):
  print "Provide input file to process"
  print sys.argv[0] + " filename.csv\n"
  sys.exit(0)


inpfilename=sys.argv[1]
outfilename="processed-" + inpfilename


with open(inpfilename,'r') as inpf, open(outfilename,'wb') as outf:

    inpreader  = csv.reader(inpf, delimiter=',')
    sanewriter = csv.writer(outf, delimiter=',')

    header = next(inpreader,None);

    # for i in range(len(header)):
    #     print i, header[i]
    # sys.exit(0)

    outheader = [ "Unique ID",
                  "Filename",
                  "SHA1 hash",
                  "Title",
                  "Creator",
                  "Date",
                  "Coverage.Temporal",
                  "Coverage.Spatial",
                  "Publisher",
                  "Description",
                  "Language",
                  "File type",
                  "Content Type",
                  "Format",
                  "Copyright",
                  "Keyword/Subject",
    ]
    sanewriter.writerow(outheader)

    
    nrows = 0
    for irow in inpreader:
        result = makesane(irow)
        if (result != "Error"):
            sanewriter.writerow(result)
            nrows += 1

print
print '===================================================='
print 'Processed', nrows, "rows"
print 'Use', outfilename, "in the migrate module"
print

    
        
