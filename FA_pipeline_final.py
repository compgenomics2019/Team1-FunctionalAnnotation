#!/usr/bin/env python3
import argparse
import os
import subprocess
from utilities import functional_annotation
from utilities import toGFF3
from utilities import clustering
from utilities import mapping
from utilities import mergeAll_to_gff
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--faa", required = True, help="The location of the directory containing all .faa files")
    parser.add_argument("-n", "--fna", required = True, help = "The location of the directory containing all .fna files")
    parser.add_argument("-a", "--asem", required = True, help="The location of the directory containing all assembly files") 
    parser.add_argument("-oa", "--annotationFolder",required = True, help="name of output containing annotation results")
    parser.add_argument("-og", "--gffFolder",required = True, help="name of output containing  gff files of each annotation tool") 
    parser.add_argument("-om", "--mergeFolder",required = True, help="name of output containing all merged gff files")
    args = parser.parse_args()

    """ In order to run DOOR2 and VFDB, we need a database, so have to check if the database is provided in current working folder """
    operonDB="operonDB.fasta"
    vfdbDB="VFDBdb.fasta"
    if not os.path.exists(operonDB) or not os.path.exists(vfdbDB):
        raise SystemExit("missing database for DOOR2 or VFDB, cannot running DOOR2/VFDB.Exit")
    """ if there is no missing required files, then run annotation """
    faa_dir=args.faa
    """ cluster for eggNOG """ 
    mergeFile_faa="merge.txt"     #file that merge all 50 genomes 
    clusterFolder="cluster_CDHIT"
    clusterFile="clusterFile.txt"
    if not os.path.exists(clusterFolder):
        clustering.main(faa_dir,mergeFile_faa,clusterFolder,clusterFile,0.95)
    """ name the output folder for each tool """
    outputFolder=args.annotationFolder
    tmhmm_out="{}/tmhmm_result".format(outputFolder)
    singalP_out="{}/signalP_result".format(outputFolder)
    door2_out="{}/door2_result".format(outputFolder)
    vfdb_out ="{}/VFDB_result".format(outputFolder)
    card_out="{}/card_result".format(outputFolder)
    piler_seq="{}/pilercr_seq".format(outputFolder)
    piler_out="{}/pilercr_result".format(outputFolder)
    eggNOG_out="{}/eggnog_result_oneFile".format(outputFolder) #contain 1 output , from annotated 1 cluster with eggnog
    eggNOG_map_out="{}/eggnog_result_allFiles".format(outputFolder)
    
    if not outputFolder in os.listdir():
        subprocess.call(["mkdir",outputFolder])
    if not door2_out.split("/")[1] in os.listdir(outputFolder): 
        #functional_annotation.door2blast_local_all50(faa_dir,operonDB,"blast_operon_db",door2_out) 
        functional_annotation.door2blast_server_all50(faa_dir,operonDB,"blast_operon_db",door2_out)
    if not vfdb_out.split("/")[1] in os.listdir(outputFolder):
        #functional_annotation.vfdbblast_local_all50(args.fna,vfdbDB,"blast_vfdb_db",vfdb_out)
        functional_annotation.vfdbblast_server_all50(args.fna,vfdbDB,"blast_vfdb_db",vfdb_out)
    if not card_out.split("/")[1] in os.listdir(outputFolder):
        functional_annotation.rgi_all50(faa_dir,card_out)
    if not tmhmm_out.split("/")[1] in os.listdir(outputFolder):      
        functional_annotation.tmhmm_all50(faa_dir,tmhmm_out)
    if not singalP_out.split("/")[1] in os.listdir(outputFolder):
        functional_annotation.signalP_all50(faa_dir,singalP_out)
    if not piler_out.split("/")[1] in os.listdir(outputFolder):      
        functional_annotation.piler_all50(args.asem,piler_seq,piler_out)
    if not eggNOG_out.split("/")[1] in os.listdir(outputFolder):
        subprocess.call(["python2","utilities/eggnog.py",eggNOG_out])


    """ EGGNOG mapping: from one output of EGGNOG, map to 50 output files for 50 faa files"""
    if not eggNOG_map_out.split("/")[1] in os.listdir(outputFolder):
        names_file="allfiles.txt" #contains 50 id number of each genome
        id_file_faa="title.txt" # contains header line in merge file that concatenate all 50 genomes faa/fna
        mapping.main(faa_dir,names_file,id_file_faa,mergeFile_faa,eggNOG_out,clusterFolder,eggNOG_map_out)
    """ after annotation all 50 files, then convert to gff for each annotation tool"""

    gff_out_folder=args.gffFolder #folder containing gff files for each annotation tool
    if not gff_out_folder in os.listdir():
        subprocess.call(["mkdir",gff_out_folder])

    tmhmm_gff,signalP_gff,piler_gff,card_gff,door2_gff,vfdb_gff,eggnog_gff="{}/tmhmm_to_gff".format(gff_out_folder),"{}/signalP_to_gff".format(gff_out_folder)\
        ,"{}/pilercf_to_gff".format(gff_out_folder),"{}/card_to_gff".format(gff_out_folder),\
         "{}/door2_to_gff".format(gff_out_folder),"{}/vfdb_to_gff".format(gff_out_folder),"{}/eggnog_to_gff".format(gff_out_folder)
   
    toGFF3.main(tmhmm_out,tmhmm_gff,singalP_out,signalP_gff,door2_out,door2_gff,vfdb_out,vfdb_gff,card_out,card_gff,piler_out,piler_gff,eggNOG_map_out,eggnog_gff,outputFolder,gff_out_folder)
    
    #if there is exist all gff folders for all tool, we can begin to merge
    all_gff_faa=args.mergeFolder
    if all_gff_faa not in os.listdir():
        mergeAll_to_gff.main(tmhmm_gff,signalP_gff,piler_gff,card_gff,door2_gff,vfdb_gff,eggnog_gff,all_gff_faa)
if __name__ == "__main__":
    main()
