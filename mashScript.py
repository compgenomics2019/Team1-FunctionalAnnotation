#!/usr/bin/env python3
import sys
import os
import argparse
import subprocess
import pandas as pd
import numpy

def dirlist(path):
    file_list = []
    path = os.path.expanduser(path)  #get absolute path if user provides relative path
    for f in os.listdir(path):
        file_list.append(os.path.join(path,f))
    return file_list
def createMatrix(fileList):
    size=len(fileList)+1
    df=[["" for i in range(size) ] for j in range(size)]   
    nameList=[os.path.basename(f) for f in fileList]
    for i in range(size-1): 
        df[0][i+1]=nameList[i]
        df[i+1][0]=nameList[i]
    return df
def mash(df,dirF):
    size=len(df[0])-1
    dirF=os.path.expanduser(dirF)
    mashOutFile=open("mashResults.txt","w")
    for row in range(1,size):
        for col in range(row+1,size):          
            rowName=os.path.join(dirF+"/"+df[row][0]) #cell in first column
            colName=os.path.join(dirF+"/"+df[0][col]) # cell in first row  
            command="{} dist {} {}".format("./mash",colName,rowName) 
            subprocess.call(command,shell=True,stdout=mashOutFile)  
    mashOutFile.close()
def editOutputFile(outFile):  
    with open(outFile,"r") as fh:
        with open("MashResults_editted.txt","w") as newFH:
            newFH.write("{}\t\t{}\t{}\t{}\t{}\n".format("genome1","genome2","Mash-distance","P-value","Matching-hashes"))
            for l in fh:
                cols=l.strip().split()
                newLine="{}\t{}\t{}\t{}\t{}\n".format(os.path.basename(cols[0]),os.path.basename(cols[1]),cols[2],cols[3],cols[4])
                newFH.write(newLine)
    os.remove("mashResults.txt")
def main():
    parser = argparse.ArgumentParser(description='FunctionalAnnotation')
    parser.add_argument('-ma',"--mash",required=False,action="store_true",help = 'Clustering by Mash')
    parser.add_argument('-v',"--vsearch" ,action="store_true",required=False,help = 'Clustering by VSEARCH')
    parser.add_argument('-d',"--dir" ,type=str,required=True,help = 'directory')
    args=parser.parse_args()
    if args.mash:         
        dirFolder=args.dir
        file_list=dirlist(dirFolder)  
        df=createMatrix(file_list)
        mash(df,dirFolder)
        editOutputFile("mashResults.txt")
if __name__ == '__main__':
	main()