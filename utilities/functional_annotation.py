#!/usr/bin/env python3
import sys
import os
import argparse
import subprocess
import re
def signalP_all50(inDir,outFolder):
    print("annotating using SingalP")
    """ annotate 50 files """
    """ if os.path.exists(outFolder):
        subprocess.call(["rm","-dr",outFolder]) """
    subprocess.call(['mkdir',outFolder])
    signalP_path="signalp-5.0/bin/signalp"
   
    for f in os.listdir(inDir):
        if "scaffolds" in f:
            inFile=os.path.join(inDir,f)
            #print("annotating signal peptide {}".format(f))
            outFile=os.path.join("{}_signalP".format(f.split(".")[0]))
            #print(outFile)
            subprocess.call([signalP_path,"-fasta",inFile,"-org","gram-","-prefix",outFile,"-gff3"])
    for f in os.listdir():
        if "_signalP.gff3" in f or "summary.signalp5" in f:
            subprocess.call(["mv",f,outFolder])
def tmhmm_all50(inDir,outFolder):
    print("annotating using TMHMM")
    """ annotate 50 files """
    """ if os.path.exists(outFolder):
        subprocess.call(["rm","-dr",outFolder]) """
    subprocess.call(['mkdir',outFolder])
    for f in os.listdir(inDir):
        if "scaffolds" in f:
            outFile= os.path.join(outFolder,"{}_tmhmm.txt".format(f.split('.')[0]))
            f=os.path.join(inDir,f)
            print(outFile)
            print("annotating transmembrane protein {}".format(f))
            tmmCommand="tmhmm-2.0c/bin/tmhmm -short {} > {} ".format(f,outFile)
            subprocess.call(tmmCommand,shell=True)  
def rgi_all50(inDir,outFolder):
    print("annotating card")
    #annotat all 50 .faa files
    """ if os.path.exists(outFolder):
        subprocess.call(["rm","-dr",outFolder])
     """
    subprocess.call(['mkdir',outFolder])
    card="card-data/card.json"
    model="card-data/protein_fasta_protein_homolog_model.fasta"
    t="protein"

    for curF in os.listdir(inDir):
        if "scaffolds" in curF:
            inFile=os.path.join(inDir,curF)
            prefix=os.path.join(outFolder,"{}_card".format(curF.split('.')[0])) 
            #print(prefix)
            print("annotating antibiotic resistance using CARD {}".format(curF))  
            subprocess.run(["rgi","load","-i",card,"--card_annotation",model,"--local"])
            subprocess.run(["rgi","main","-i",inFile,"-o",prefix,"--input_type",t,"--local"])
            allFiles=os.listdir(os.getcwd()) #list all files in the current working directory """
      
    for f in os.listdir(outFolder):
        if ".xml" in f or ".json" in f:
            subprocess.call(["rm",os.path.join(outFolder,f)])
def piler_all50(inDir,seqFolder,outFolder):
    print("annotating using PIler")
    #annotate all 50 ASSEMBLY files
    """ if os.path.exists(outFolder):
        subprocess.call(["rm","-dr",outFolder])
    if os.path.exists(seqFolder):
        subprocess.call(["rm","-dr",seqFolder])  """ 
    subprocess.call(['mkdir',outFolder])
    subprocess.call(['mkdir',seqFolder])
    for f in os.listdir(inDir):
        if "scaffolds" in f:           
            inputseq = os.path.join(inDir,f)
            out = os.path.join(outFolder,"{}_pilercr".format(f.split('.')[0]))
            sequ = os.path.join(seqFolder,"{}.fasta".format(f.split('.')[0]))
            subprocess.call(['pilercr1.06/pilercr','-in',inputseq,'-out',out,'-seq',sequ])

def vfdbblast_server_all50(inDir,vfdbDB,database,outFolder):
    print("annotating virulence factors")
    subprocess.call(['mkdir',outFolder])
    if not os.path.exists(database):
        dbDir=os.path.join(database,"myDatabase")
        subprocess.call(["ncbi-blast-2.8.1+/bin/makeblastdb","-in",vfdbDB,"-input_type","fasta","-dbtype", "nucl", "-out",dbDir,"-title","create virulence factor database"])      
    else:# if  database already exists
        dbDir=os.path.join(database,"myDatabase")

    for f in os.listdir(inDir):
        if "scaffolds" in f:
            outFile= os.path.join(outFolder,"{}_vfdb.txt".format(f.split('.')[0]))
            inFile=os.path.join(inDir,f) 
            print("annotating virulent factors {}".format(f))
            subprocess.call(["ncbi-blast-2.8.1+/bin/blastn" ,"-db", dbDir, "-query", inFile , "-num_threads","4", "-evalue" ,"1e-10", "-outfmt", "6 stitle qseqid pident qcovs qstart qend qseq evalue bitscore", \
                "-best_hit_score_edge", "0.1", "-best_hit_overhang", "0.1","-max_target_seqs", "1", "-out", outFile])
def vfdbblast_local_all50(inDir,vfdbDB,database,outFolder):
    print("annotating virulence factors")
    if os.path.exists(outFolder):
        subprocess.call(["rm","-dr",outFolder])
    subprocess.call(['mkdir',outFolder])
    if not os.path.exists(database):
        dbDir=os.path.join(database,"myDatabase")
        subprocess.call(["makeblastdb","-in",vfdbDB,"-input_type","fasta","-dbtype", "nucl", "-out",dbDir,"-title","create virulence factor database"])      
    else:# if  database already exists
        dbDir=os.path.join(database,"myDatabase")
    for f in os.listdir(inDir):
        
        if "scaffolds" in f:
            outFile= os.path.join(outFolder,"{}_vfdb.txt".format(f.split('.')[0]))
            inFile=os.path.join(inDir,f) 
            print("annotating virulent factors {}".format(f))
            subprocess.call(["blastn" ,"-db", dbDir, "-query", inFile , "-num_threads","4", "-evalue" ,"1e-10", "-outfmt", "6 stitle qseqid pident qcovs qstart qend qseq evalue bitscore", \
                "-best_hit_score_edge", "0.1", "-best_hit_overhang", "0.1","-max_target_seqs", "1", "-out", outFile])
def door2blast_local_all50(inDir,operonDB,database,outFolder):
    print("annotating operons")
    """ if os.path.exists(outFolder):
        subprocess.call(["rm","-dr",outFolder]) """
    subprocess.call(['mkdir',outFolder])
    if not os.path.exists(database):
        dbDir=os.path.join(database,"myDatabase")
        subprocess.call(["makeblastdb","-in",operonDB,"-input_type","fasta","-dbtype", "prot", "-out",dbDir,"-title","create operon database"])      
    else:# if  database already exists
        dbDir=os.path.join(database,"myDatabase")

    for f in os.listdir(inDir):
        if "scaffolds" in f:
            outFile= os.path.join(outFolder,"{}_door2.txt".format(f.split('.')[0]))
            #print(outFile)
            inFile=os.path.join(inDir,f)
            print("annotating operon using DOOR2 {}".format(f))
            subprocess.call(["blastp" ,"-db", dbDir, "-query", inFile , "-num_threads","4",\
                 "-evalue" ,"1e-10", "-outfmt", "6 stitle qseqid pident qcovs qstart qend qseq evalue bitscore", "-best_hit_score_edge", "0.1", "-best_hit_overhang", "0.1","-max_target_seqs", "1", "-out", outFile])
def door2blast_server_all50(inDir,operonDB,database,outFolder):
    print("annotating operons")
    """ if os.path.exists(outFolder):
        subprocess.call(["rm","-dr",outFolder]) """
    subprocess.call(['mkdir',outFolder])
    if not os.path.exists(database):
        dbDir=os.path.join(database,"myDatabase")
        subprocess.call(["ncbi-blast-2.8.1+/bin/makeblastdb","-in",operonDB,"-input_type","fasta","-dbtype", "prot", "-out",dbDir,"-title","create operon database"])      
    else:# if  database already exists
        dbDir=os.path.join(database,"myDatabase")

    for f in os.listdir(inDir):
        if "scaffolds" in f:
            outFile= os.path.join(outFolder,"{}_door2.txt".format(f.split('.')[0]))
            #print(outFile)
            inFile=os.path.join(inDir,f)
            print("annotating operon using DOOR2 {}".format(f))
            subprocess.call(["ncbi-blast-2.8.1+/bin/blastp" ,"-db", dbDir, "-query", inFile , "-num_threads","4",\
                 "-evalue" ,"1e-10", "-outfmt", "6 stitle qseqid pident qcovs qstart qend qseq evalue bitscore", "-best_hit_score_edge", "0.1", "-best_hit_overhang", "0.1","-max_target_seqs", "1", "-out", outFile])
def removeFiles(inDir):
    """ this function is to remove intermediate files in the output folder after ruuning annotatioin """        
    for f in os.listdir(inDir):
        f=os.path.join(inDir,f)
        if ".xml" in f or ".json" in f:
            subprocess.call(["rm",f])

