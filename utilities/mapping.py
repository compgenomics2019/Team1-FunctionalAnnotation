#!/usr/bin/env python3
import subprocess
import re
import os
import random
""" The input file is the output file after running EGGNOG
        This function is  to extract the relationship between centroid sequences and each sample's gene id
        The output files are "1020.txt,1785.txt ...", you can open these files to learn more about this
     """
def getTitleFile(title_file, clusterFolder,mergeFile):
    print("creating title file")
    mergeFile=os.path.join(clusterFolder,mergeFile)
    with open(title_file,"w") as outFH:
        with open(mergeFile,"r") as fh:
            for l in fh:
                if l.startswith(">"):
                    outFH.write(l)

def get_all_seqs_name(inDir,newFile):
    """ this function is to extract genome name to make a file that contain each line as a genome name. Ex 1020 /n /1222 """
    print("creating ids file")
    a_list=[]
    with open(newFile,"w") as fh:
        for f in os.listdir(inDir):
            if ".faa" in f:
                name=f.split("_")[0]
                a_list.append(name)
        a_list.sort()
        for n in a_list:
            fh.write(n+"\n")
def get_cluster_files(clusterFolder,names_file,outDir):
    print("creating cluster files")
    cluster_file=""
    for f in os.listdir(clusterFolder):
        if f.endswith(".txt.clstr"):
            cluster_file=os.path.join(clusterFolder,f)
    file =open(cluster_file,"r") # open the "clusterFile.txt.clstr" file
    files=file.read() #read as one string
    x=files.split(">Cluster")
    alllist=open(names_file,"r") # open the "allfiles.txt"
   
    #print(x[:5])
    def main(input_samples):
        tmp=[]
        name_list=[]
        for i in x[1:]: #dont look at the centroid sequence      
            y=i.split('\n')[1:]
            for i in y:
                if i!='':
                    z=i.split(', ')[1]
                    zz=z.split('...')[0]
                    tmp.append(zz)
            name_list.append(tmp)
            #print(name_list)
            tmp=[]

        output=[]
        #print(name_list)
        for i in name_list:
            if i[0].startswith('>%s'%(input_samples)): # ADD
                output.append([i[0],i[0]])                        #ADD
            for j in i[1:]:
                if j.startswith('>%s'%(input_samples)):
                    output.append([i[0],j])
        #outfiles=open("%s.txt"%(input_samples),"w") # write output files looks like "1020.txt,1785.txt, ..."
        outfiles=open("{}/{}_cluster.txt".format(outDir,input_samples),"w")
        count=0
        for i in output: #is is ['>1365:NODE_11_length_168224_cov_22.876340_82', '>1032:NODE_6_length_239963_cov_14.069204_76']            
            count+=1
            outfiles.write("#%s\n"%(count))
            for j in i:
                outfiles.write("%s\n"%(j))

    for line in alllist:          # run the main function
        input_info=line.split('\n')[0]
        main(input_info)

def mapping_to_50files(eggNOG_Dir,outDir):
    print("mapping 1 eggnog output to 50 eggnog output")
    subprocess.call(["mkdir",outDir])
    eggnogFile=""
    cluster=[]
    for f in os.listdir(eggNOG_Dir):
        if "eggnogOutput" in f:
            eggnogFile=os.path.join(eggNOG_Dir,f)
    file=open(eggnogFile,"r")
    next(file)
    next(file)
    next(file)
    egg_title=next(file)  #this files contains the title for eggnog, This is not necessary. only one line "gene_id, annotation info..." inside this file
    for line in file: # put all the info in eggnog to a list named 'cluster', this list looks like [[gene_id1,[annotationinfo...],[gene_id2,[annotationinfo...]...]
        x=">%s"%(line.split('\t')[0])
        y=line.split('\t')[1:]
        cluster.append([x,y])
    #print(cluster)
    for f in os.listdir(eggNOG_Dir):
        if "_cluster.txt" in f:
            dict_in={}  #key is number of cluster, value is pair ['>1743:NODE_42_length_27761_cov_25.415575_1', '>1357:NODE_39_length_27683_cov_15.459828_12']
            file_input=open(os.path.join(eggNOG_Dir,f),"r") #open('%s.txt'%(f),'r') # open a file (e.g. 1020.txt, 1785.txt,..) that contains both the centroid gene id and related 
            count=-1
            for line in file_input: # add the
                if line.startswith('#'):
                    count+=1
                    continue
                elif line.startswith('>') and count not in dict_in:
                    x=re.sub('\n',repl='',string=line)
                    dict_in[count]=[x]
                elif line.startswith('>') and count in dict_in:
                    x=re.sub('\n',repl='',string=line)
                    dict_in[count]=dict_in[count]+[x]
            
            input_list=[]
            #print(dict_in.values())
            for values in dict_in.values():
                input_list.append(values) #input_list contains list of list ['>1358:NODE_60_length_12023_cov_11.960478_3', '>1595:NODE_61_length_12023_cov_10.910762_2'], ['
            #print(input_list[:3])
            output=[] #list of list contains '>1365:NODE_1_length_430394_cov_23.539821_1', ['155864.Z5598', '3e-97', '316.2', 'YJAB', '', 'K03827', '', 'bactNOG[38]', '05K5X@bactNOG,0QQJ2@gproNOG,17CRJ@proNOG,COG0454@NOG', '05K5X|5.33513221566e-63|216.752120972', 'K', 'acetyltransferase\n']]
            for i in input_list:
                for j in cluster:
                    if i[0]==j[0]:
                        output.append([i[1],j[1]])
            #print(output[:2])
            final_out=[]
            egtitle=[]
            for line in egg_title:
                final_out.append(line)
            for i in output:
                #x='\t'.join(i[1])
                x='\t'.join(i[1])
                y='%s\t%s'%(i[0],x)
                final_out.append(y)
            #print(final_out[0])
            outFileName=os.path.join(outDir,'{}_eggnog.txt'.format(f.split("_")[0]))
            outFile=open(outFileName,'w')
            for i in final_out:
                outFile.write(i)
    #print(dict_in[0])
def main(faa_dir,names_file,title_file,mergeFile,eggNOG_Dir,clusterFolder,outMapDir):
    """ eggNOG_Dir is the new folder containing multiple cluster, each cluster contains one line from the cluster file,
     one line contains the corresponding header with the centroid header in the .clsr file, for each genome, specifically faa file """
    names_file=os.path.join(eggNOG_Dir,names_file)
    
    if not os.path.exists(names_file):
        get_all_seqs_name(faa_dir,names_file)

    flag=1 #for not create cluster files
    if flag == 1:
        get_cluster_files(clusterFolder,names_file,eggNOG_Dir)
        flag=0

    mapping_to_50files(eggNOG_Dir,outMapDir)
    title_file=os.path.join(outMapDir,title_file)
    #print(names_file,title_file)
    if not os.path.exists(title_file):
        getTitleFile(title_file, clusterFolder,mergeFile)