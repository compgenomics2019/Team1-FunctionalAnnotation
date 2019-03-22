#!/usr/bin/env python3
import sys
import os,glob
import argparse
import subprocess
import re
from Bio import Entrez
import urllib3

def transmembranePrediction(tmmPath,form,inFile,outputFile):
    """ the input file is the FASTA file , tmmPath is the path for ../tmmhmm2.0c/tmhmm"""
    
    if os.path.exists(inFile):
        if os.path.exists(outputFile):
            subprocess.call(["rm",outputFile])
        tmmCommand="{} -{} {} > {} ".format(tmmPath,form,inFile,outputFile)
        subprocess.call(tmmCommand,shell=True)
    else:
        raise SystemExit("There is no input Fasta file. Exit program")
def outputToGff(outputFile):
    """ convert outputFile from annotation tool that is not in gff file ( like TMHMM tool) """
    return 0
def rgi_function(card,model,main_input,prefix,t):
        subprocess.run(["rgi","load","-i",card,"--card_annotation",model,"--local"])
        subprocess.run(["rgi","main","-i",main_input,"-o",prefix,"--input_type",t,"--local"])
        allFiles=os.listdir(os.getcwd()) #list all files in the current working directory
        for f in allFiles:
            temp=re.search(r".temp.",f)
            if temp:
                os.remove(f)
def extractSeqFromGID(operonFile):
    #make a list to store all ids
    idList = []  # list to store id
    with open(operonFile, 'r') as fh:
        lines = fh.readlines()
        index = 0
        while not lines[index].startswith("OperonID"):
            index += 1
        index +=1
        llen = len(lines)
        while index < llen:
            words = lines[index].split()
            if len(words) > 1:
                idList.append(words[1])
            index += 1
    #fetch sequences based on gid
    Entrez.email = "yhuang690@gatech.edu"
    handle = Entrez.efetch(db="nucleotide", id = idList, rettype="fasta", retmode="text")
    line = handle.readline()
    fileo = open("operonDB.fasta", "w")
    while line :
        fileo.write(line)
        line = handle.readline()
    handle.close()
    fileo.close()
def door2blast(inFile,outFile):
    subprocess.call(["makeblastdb","-in","operonDB.fasta","-input_type","fasta","-dbtype", "prot", "-out","myDatabase","-title","create operon database"]) #outTemp is output from makeblastdb
    #subprocess.call(["makeblastdb","-in","operonDB.fasta","-input_type","fasta","-dbtype", "prot", "-parse_seqids","-out","outTemp","-title","create operon database"])
    """ if os.path.exists("temp"):
        subprocess.call(["rm","-dr","temp"])
    subprocess.call(["mkdir", "-p","temp"]) """
    subprocess.call(["blastp","-db","myDatabase","-query",inFile,"-num_threads","4","-evalue","1e-10","-outfmt","6","-max_target_seqs","1","-out",outFile])
    #rm all intermediate files from makeblastdb
    dbfiles=[f for f in os.listdir() if f.startswith("myDatabase.")]
    for f in dbfiles:
        subprocess.call(["rm",f])
def main():
    parser = argparse.ArgumentParser(description='FunctionalAnnotation')
    #parser for transmembrane annotation TMHMM
    parser.add_argument("-tmhmm",required=False, help="path for tmhmm2.0-c/bin/tmhmm")
    parser.add_argument("-i","--input",required=False, help="input FASTA file for annotation") 
    parser.add_argument('-o',"--output", action="store",help='Merging all .fna files into 1 files')
    parser.add_argument("-form",action="store_true",default = "short",required=False, help="path for tmhmm2.0-c/bin/tmhmm")
    #parser for CARD
    parser.add_argument("-rgi",action="store_true",required=False,help="antibiotic resistance annotation by RGI")
    parser.add_argument('-i_card_json',help='path to card.jason',required=False,type=str)
    parser.add_argument('-i_model',help='path to homology model',required=False,type=str)
    #parser.add_argument('-i_main',help='path to fasta file',required=False,type=str)
    #parser.add_argument('-o_prefix',help='ouput prefix',required=False,type=str)
    parser.add_argument('-type',help='read,contig,protein,wgs',required=False,type=str)  
    #parser for door2: -
    parser.add_argument("-door2",action="store_true",required=False,help="annotating operon by DOOR2")
    parser.add_argument('-table',help='operon table',required=False) 

    args=parser.parse_args()
    if args.rgi:
        """ card=args.i_card_json
        model=args.i_model
        main_input=args.input
        prefix=args.output
        t=args.type """

        if args.input == None: 
            raise SystemExit("missing input file. Exit")
        if args.output == None :
            args.output ="rgiOut.txt" #default
        rgi_function(args.i_card_json,args.i_model,args.input,args.output,args.type)
    if args.tmhmm:
        if args.input == None :
            raise SystemExit("missing input file. Exit")
        if args.output == None :
            args.output ="tmhmmOut.txt" #default
        if args.form != "short":
            if args.form !="long":
                raise SystemExit('format can only be either "long" or "short" ' )      
        transmembranePrediction(args.tmhmm,args.form,args.input,args.output)
    if args.door2:
        if args.table == None and os.path.exists("operonDB.fasta"):
            print('not creating fasta file')
            pass
        elif args.table == None and not os.path.exists("operonDB.fasta"):
            raise SystemExit("missing operon table. Exit program")
        elif args.table != None :
            extractSeqFromGID(args.table) #overwirte operonDB.fasta if exits or create operonDB.fasta file

        if args.input == None:
            raise SystemExit("missing input fasta file")
        if args.output == None:
            args.output = "door2_Out"  #name of default output
        door2blast(args.input,args.output) #args.input is the fasta file of genome
if __name__ == '__main__':
	main()