#!/usr/bin/env python3
import sys
import os
import argparse
import subprocess
import re

def mergeFiles(path,mergedFile):
    path = os.path.expanduser(path)
    with open(mergedFile,"w") as fh:
        for curFile in os.listdir(path):
            if (not curFile.startswith(".")):
                curFile_fullpath=os.path.join(path,curFile)
                with open(curFile_fullpath,"r") as curFH:
                    for curLine in curFH:
                        header=re.search("\>(.*)",curLine)
                        if header:
                            newHeader="{}{}:{}\n".format(">",curFile.split(".")[0],header.group(1))
                            fh.write(newHeader)
                        else:
                            #remove . at the beginning of line
                            if curLine.startswith("."):
                                curLine=curLine.replace(".","")#curLine[1:]                                                         
                            fh.write(curLine)
def vsearchCluster(mergeFile):
    #print(os.getcwd())
    if os.path.exists(mergeFile):
        vDir="./vsearchFiles"
        if os.path.exists(vDir):
            subprocess.call(["rm","-dr",vDir])
        subprocess.call(["mkdir",vDir])
        centroidFile=os.path.join(vDir,"mergeCentroid.fa")
        outFile=os.path.join(vDir,"mergeOut.txt")
        idNum=0.97
        command="vsearch --cluster_fast {} --centroids {} --msaout {} --id {}".format(mergeFile,centroidFile,outFile,idNum)
        subprocess.call(command,shell=True)
    else:
        raise SystemExit ("there is no input merge File")
def mmseqsCluster(mergeFile):
    if os.path.exists(mergeFile):
        mDir="./mmseqFiles"
        if os.path.exists(mDir):
            subprocess.call(["rm","-dr",mDir])
        subprocess.call(["mkdir",mDir])
        os.chdir(mDir) #change directory to mmseqFiles
        mergeFile=os.path.join("..",mergeFile)
        makeDatabase = "mmseqs createdb {} {}".format(mergeFile,"DB")
        subprocess.call(makeDatabase,shell=True)
        tmpFile="./tmp"
        subprocess.call(["mkdir",tmpFile])
        subprocess.call(["mmseqs","cluster","DB","DB_clu",tmpFile]) 
        #create  output file
        subprocess.call(["mmseqs", "createtsv", "DB", "DB", "DB_clu", "DB_clu.tsv"])
        print("done1")
        try:
            subprocess.call(["mmseqs","createseqfiledb","DB","DB_clu","DB_clue_seq"])
        except:
            print("not done2")
        else:
            subprocess.call(["mmseqs","result2flat","DB","DB","DB_clu_seq","DB_clue_seq.fasta"])
    else:
        raise SystemExit ("there is no input merge File")
def transmembranePrediction(inFile,tmmPath):
    """ the input file is the FASTA file , tmmPath is the path for ../tmmhmm2.0c/tmhmm"""
    if os.path.exists(inFile):
        outputFile="tmhmmOutput.txt"
        if os.path.exists(outputFile):
            subprocess.call(["rm",outputFile])
        tmmCommand="{} {} > {} ".format(tmmPath,inFile,outputFile)
        subprocess.call(tmmCommand,shell=True)
    else:
        raise SystemExit("There is no input Fasta file. Exit program")
def main():
    parser = argparse.ArgumentParser(description='FunctionalAnnotation')
    parser.add_argument('-me',"--merge" ,action="store_true",help = 'Merging all .fna files into 1 files')
    parser.add_argument('-o',"--output", action="store",help='Merging all .fna files into 1 files')
    parser.add_argument('-d',"--dir" ,type=str,required=False,help = 'directory for files to merge')
    parser.add_argument('-v',"--vsearch" ,action="store_true",required=False,help = 'cluster by vsearch')
    parser.add_argument('-ms',"--mmseqs" ,action="store_true",required=False,help = 'cluster by MMSEQS')
    parser.add_argument("-t","--tmhmm",required=False, help="predict transmembrane proteins by TMHMM")
    parser.add_argument("-i","--input",required=False, help="input FASTA file for annotation")
    args=parser.parse_args()
    
    if args.merge:         
        dirFolder=args.dir 
        mergeFiles(dirFolder,args.output)
    if args.vsearch:
        vsearchCluster(args.input)
    if args.mmseqs:
        mmseqsCluster(args.input)
    if args.tmhmm:
        transmembranePrediction(args.input,args.tmhmm)
if __name__ == '__main__':
	main()