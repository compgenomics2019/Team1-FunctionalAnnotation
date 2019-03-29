#!/usr/bin/env python3
import sys
import os
import argparse
import subprocess
import re
import random
random.seed(100)
def getMergedFile(inDir,outFolder,mergeFile):
    if os.path.exists(outFolder):
        pass     
    else: 
        subprocess.call(['mkdir',outFolder])
    with open(mergeFile,"w") as fh:
        for curFile in os.listdir(inDir):
            if ".faa" in curFile: #avoid .DS file
                curFile_fullpath=os.path.join(inDir,curFile)
                with open(curFile_fullpath,"r") as curFH:
                    for curLine in curFH:
                        #header=re.search("\>(.*)",curLine)
                        if curLine.startswith(">"):
                            #newHeader="{}{}:{}\n".format(">",curFile.split(".")[0],header.group(1))
                            #newHeader=curLine.strip()+":"+curFile.split("_")[0]+"\n"
                            newHeader=">"+curFile.split("_")[0]+":"+curLine.strip()[1:]+":"+"\n"
                            #print(newHeader)
                            fh.write(newHeader)
                        else:
                            #remove . at the beginning of line
                            """ if curLine.startswith("."):
                                curLine=curLine.replace(".","")#curLine[1:]   """                                                       
                            fh.write(curLine)
    subprocess.call(["mv",mergeFile,outFolder])
def shuffleMergeFile(mergeFile,newFile):
    """ I want to shuffle the sequences before runing cd hit (multiple step clustering)"""
    # allSeqs=[] #

    # with open(mergeFile,"r") as fh:
    #     oneString=fh.read().strip()
    #     allSeqs=oneString.split(">")[1:]
    #     for i in range(10):
    #         random.shuffle(allSeqs)
    # with open(newFile,"w") as fh:
    #     for one_seq in allSeqs:
    #         lines=one_seq.split("\n")
    #         header=">{}\n".format(lines[0])
    #         seq="".join(lines[1:])
    #         fh.write(header)
    #         fh.write(seq+"\n")
    a_dict={}
    with open(mergeFile,"r") as fh:
        for l in fh:
            if l.rstrip().startswith(">"):
                header=l
                if l not in a_dict:
                    a_dict[header]=[]
            else:
                a_dict[header].append(l.rstrip())
    a_list=list(a_dict.keys())
    random.shuffle(a_list)
    with open(newFile,"w") as fh:
        for k in a_list:
            fh.write(">"+k)
            for l in a_dict[k]:
                fh.write(l+"\n")
def clusterByCDHIT(clusterFolder,inFile,outFile,threshold):
    #inFile=os.path.join(clusterFolder,inFile)
    outFile=os.path.join(clusterFolder,outFile)
    n=0
    if int(threshold) >1:
        raise SystemExit("similar identity can only be from 0 to 1. exit")
    subprocess.call(["cd-hit","-i",inFile,"-o",outFile,"-n","5","-g","1","-d","150"])
    #subprocess.call(["mv",clusterFile,clusterFolder])
def main(inFaaDir,mergeFile,clusterFolder,clusterFile,threshold):
    print("clustering 50 genomes using CD-HIT")
    mergeFile=os.path.join(clusterFolder,mergeFile)
    if not os.path.exists(mergeFile):
        getMergedFile(inFaaDir,clusterFolder,mergeFile)
    """ shuffleFile="merge2.txt"
    if not os.path.exists(os.path.join(clusterFolder,shuffleFile)):
        shuffleMergeFile(mergeFile,os.path.join(clusterFolder,shuffleFile)) """
    
    #clusterByCDHIT(clusterFolder,os.path.join(clusterFolder,shuffleFile),clusterFile,threshold)
    clusterByCDHIT(clusterFolder,mergeFile,clusterFile,threshold)
    #subprocess.call(["rm",mergeFile])
    #subprocess.call(["rm",os.path.join(clusterFolder,shuffleFile)])
if __name__ == '__main__':
	main()
