#!/usr/bin/env python3
import subprocess
import re
import os

def pilerToGff(inDir,newDir):
    """ the inDir is the folder containing output of piler annotation """
    """ if os.path.exists(newDir):
        subprocess.call(["rm","-dr",newDir]) """
    print("convert piler result in {} to gff".format(inDir))
    subprocess.call(['mkdir',newDir])

    for f in os.listdir(inDir):
        inFile=os.path.join(inDir,f)
        information_CRISPR = {}
        with open(inFile, "r") as crisprfile:
            for line in crisprfile:
                if "SUMMARY BY POSITION" in line:
                    for line in crisprfile:
                        information_crispr_repeat = {}
                        if line.startswith('>'):
                            head=line.strip("\n").strip(">")
                            #print(head)
                        hi = re.compile('^\s+\d+\s+(\w+)\s+(\d+)\s+(\d+)\s+\d+\s+\d+\s+\d+\s+(\d?\s+)\s+(\w+)')
                        if hi.search(line):
                            line=re.sub('\s+', '\t', line).strip().split("\t")
                            if line[7].isdigit():
                                line.remove(line[7])
                            information_crispr_repeat['start']=line[2]
                            information_crispr_repeat['end'] = int(line[2]) + int(line[3])
                            information_crispr_repeat['repeat'] = line[7]
                            information_CRISPR["{}+{}".format(head,line[0])] = information_crispr_repeat
                    #print(information_crispr_repeat)
        #print(information_CRISPR)
        outForm = os.path.join(newDir,f.split("_")[0])
        outFile=open("{}_piler.gff".format(outForm),"w+")
        outFile.write("##gff-version 3\n")
        for i,j in information_CRISPR.items():
            outFile.write("{}\tPILER-CR\tCRISPR\t{}\t{}\t.\t.\t.\t{}\n".format(i.split("+")[0],j['start'],j['end'],j['repeat']))
        outFile.close()
def tmhmmToGff(inDir,newDir):
    """ the inDir is the folder containing output of TMHMM annotation """
    print("convert tmhmm result in {} to gff".format(inDir))
    """ if os.path.exists(newDir):
        subprocess.call(["rm","-dr",newDir]) """
    subprocess.call(['mkdir',newDir])

    for f in os.listdir(inDir):
        if not f.startswith("."): #avoid .DS store
            inFile=os.path.join(inDir,f)
            bigTMHMM_info={} #dictionary with key is name of sequence, value is what should be in each line of gff file. Value is multiple values, each value is each line in gff
            with open(inFile,"r",encoding='latin-1') as fh:
                for line in fh.readlines():
                    if line.startswith("NODE"):
                        cols=line.rstrip().split("\t")
                        header=cols[0]
                        #heads=head.split("_")[:-1]
                        #header="".join(heads)   
                        if int(cols[4].split("=")[1]) != 0: #if predHEl != 0, then there is a transmembrane
                            if header not in bigTMHMM_info:
                                    bigTMHMM_info[header]=[]
                            else:
                                continue                            
                            pos=cols[5].split("=")[1] #get after Topology=
                            pos=pos.replace("i","|")
                            pos=pos.replace("o","|")
                            subPos=pos[1:-1].split("|")
                            subTMHMM_info={}
                            for i in range(0,len(subPos)):
                                subTMHMM_info={}
                                subTMHMM_info['start']=subPos[i].split("-")[0] 
                                subTMHMM_info['end']=subPos[i].split("-")[1]                                                              
                                bigTMHMM_info[header].append(subTMHMM_info)
            outForm = os.path.join(newDir,f.split("_")[0])
            outFile=open("{}_tmhmm.gff".format(outForm),"w+")
            outFile.write("##gff-version 3\n")
            for k,values in bigTMHMM_info.items():
                for val in values:
                    outLine="{}\tTMHMM\ttransmembrane protein\t{}\t{}\t.\t.\t.\t.\n".format(k,val["start"],val["end"])
                    outFile.write(outLine)
            outFile.close()
def door2toGff(inDir,newDir):
    print("convert door2 result in {} to gff".format(inDir))
    """ if os.path.exists(newDir):
        subprocess.call(["rm","-dr",newDir]) """
    subprocess.call(['mkdir',newDir])

    for f in os.listdir(inDir):
        if "scaffolds_door2.txt" in f:
            inFile=os.path.join(inDir,f)
            outForm = os.path.join(newDir,f.split("_")[0])
            outFile=open("{}_door2.gff".format(outForm),"w+")
            outFile.write("##gff-version 3\n")
            with open(inFile,"r",encoding='latin-1') as fh:
                for l in fh.readlines():
                    l=l.strip("\n").split("\t")
                    notes=l[0]
                    seqid=l[1]
                    start=l[5]
                    end=l[8]
                    outFile.write("{}\tDOOR2-BLAST\tOpeon genes\t{}\t{}\t.\t.\t.\t{}\n".format(seqid,start,end,notes))
            outFile.close()
def rgiToGff(inDir,newDir):
    print("convert card result in {} to gff".format(inDir))
    """ if os.path.exists(newDir):
        subprocess.call(["rm","-dr",newDir]) """
    subprocess.call(['mkdir',newDir])

    for i in os.listdir(inDir):
        if "card.txt" in i:
            input = os.path.join(inDir,i)
            f=open(input,'r',encoding='latin-1')
            outForm = os.path.join(newDir,i.split("_")[0])
            #outForm = os.path.join(newDir,i.split("_")[1])
            output=open("{}_rgi.gff".format(outForm),"w")
            output.write("##gff-version  3\n")
            next(f)
            f=f.readlines()
            for line in f:
                line=re.sub('\s+', '\t', line).strip().split("\t")
                #print(line)
                seqid=line[0]
                start=line[2]
                end=line[4] 
                notes=line[12:-5]
                notes=';'.join(notes)
                output.write("{}\tRGI-CARD\tAntibiotic resistant genes\t{}\t{}\t.\t.\t.\t{}\n".format(seqid,start,end,notes))      
def signalPToGFF(inDir,gffDir):
    """ signalP already genereateds gff. However, in the signalP_results folder, there are .summary.signalp5. So this function does:
    1. Move all .gff3 to specific folder
     """
    """ if os.path.exists(gffDir):
        subprocess.call(["rm","-dr",gffDir]) """
    subprocess.call(['mkdir',gffDir])

    """ if os.path.exists(newDir):
        subprocess.call(["rm","-dr",newDir])
    subprocess.call(['mkdir',newDir]) """
    #move all gff3 to gffDir folder
    for f in os.listdir(inDir):
        if "signalP.gff3" in f:
            f=os.path.join(inDir,f)
            subprocess.call(["cp",f,gffDir])


    """  for f in os.listdir(gffDir):
        if (".gff3") in f:
            #outForm = os.path.join(newDir,f)
            outFile=open(os.path.join(newDir,f),"w+")
            outFile.write("##gff-version 3\n")
            if ".gff3" in f:
                with open(os.path.join(inDir,f),"r") as fh:
                    for line in fh:
                        if line.startswith("NODE"):
                            cols=line.rstrip().split("\t")
                            #print(len(cols[1:]))
                            head=cols[0]
                            heads=head.split("_")[:-1]
                            header="".join(heads)
                            newLine=header+"\t"+"\t".join(cols[1:])
                            outFile.write(newLine+"\n") """
    #subprocess.call(["rm","-dr",gffDir]) 
def vfdbtoGff(inDir,newDir): 
    print("convert vfdb result in {} to gff".format(inDir))
    """ if os.path.exists(newDir):
        subprocess.call(["rm","-dr",newDir]) """
    subprocess.call(['mkdir',newDir]) 
    for f in os.listdir(inDir):
        inFile=os.path.join(inDir,f)
        #print(inFile) 
        outForm = os.path.join(newDir,inFile.split("/")[-1].split(".")[0].split("_")[0])    
        #outForm = os.path.join(newDir,f.split("_")[0])
        outFile=open("{}_vfdb.gff".format(outForm),"w+")
        #print(outForm)
        outFile.write("##gff-version 3\n")
        with open(inFile,"r",encoding='latin-1') as fh:
            for l in fh.readlines():
                l=l.strip("\n").split("\t")
                notes=l[0]
                seqid=l[1]
                start=l[5]
                end=l[8]
                outFile.write("{}\tVFDB-BLAST\tBacterial Virulent genes\t{}\t{}\t.\t.\t.\t{}\n".format(seqid,start,end,notes))
        outFile.close()   
def eggNOG_to_gff(inDir,newDir):
    print("convert eggNOG result in {} to gff".format(inDir))
    if os.path.exists(newDir):
        subprocess.call(["rm","-dr",newDir])
    subprocess.call(["mkdir",newDir])

    title = open('{}/title.txt'.format(inDir),'r')
    title=title.readlines()
    title_starstop=[]
    for i in title:
        i=i.split(" ")
        #print(len(i))
        title_starstop.append([i[0],i[2],i[4]])
    #print(title_starstop)
    for file in os.listdir(inDir):
        if "eggnog" in file:
            sample=open('{}/{}'.format(inDir,file),'r')
            next(sample)
            sample=sample.readlines()
            sample_annot=[]
            for i in sample:
                sample_annot.append(i.strip("\n").split("\t"))
                #break
            outForm = os.path.join(newDir,file.split("/")[-1].split(".")[0].split("_")[0])    
            #sampleout=open("{}/{}".format(newDir,file.split("_")),"w+")
            sampleout=open("{}_eggnog.gff".format(outForm),"w+")
            sampleout.write("##gff-version 3\n")
            for i in title_starstop:
                for j in sample_annot:
                    if i[0]==j[0]:
                        #sampleout.write("{}\teggnog\t{}\t{}\t{}\t.\t.\t.\t.\n".format(i[0].split(":")[1],j[-1],int(i[1]),int(i[2])))
                        sampleout.write("{}\teggNOG\t{}\t{}\t{}\t.\t.\t.\t.\n".format(i[0].split(":")[1],int(i[1]),int(i[2]),j[-1]))
                    #break
                                      
def main(tmhmm_dir,tmhmm_gff,singalP_dir,signalP_gff,door2_dir,door2_gff,vfdb_dir,vfdb_gff,card_dir,card_gff,piler_dir,piler_gff,eggNOG_dir,eggnog_gff,inFolder,outFolder):  
    #print("converting to gff for all tools") 
    
    if piler_dir.split("/")[1] in os.listdir(inFolder) and not piler_gff.split("/")[1] in os.listdir(outFolder):
        pilerToGff(piler_dir,piler_gff)
    if card_dir.split("/")[1] in os.listdir(inFolder) and not card_gff.split("/")[1] in os.listdir(outFolder):
        rgiToGff(card_dir,card_gff)
    if door2_dir.split("/")[1] in os.listdir(inFolder) and not door2_gff.split("/")[1]  in os.listdir(outFolder):
        door2toGff(door2_dir,door2_gff)
    if singalP_dir.split("/")[1] in os.listdir(inFolder) and not signalP_gff.split("/")[1]  in os.listdir(outFolder):
        signalPToGFF(singalP_dir,signalP_gff)
    if tmhmm_dir.split("/")[1] in os.listdir(inFolder) and not tmhmm_gff.split("/")[1]  in os.listdir(outFolder):
        tmhmmToGff(tmhmm_dir,tmhmm_gff)
    if vfdb_dir.split("/")[1] in os.listdir(inFolder) and not vfdb_gff.split("/")[1]  in os.listdir(outFolder) :
        vfdbtoGff(vfdb_dir,vfdb_gff)
    if eggNOG_dir.split("/")[1] in os.listdir(inFolder) and not eggnog_gff.split("/")[1]  in os.listdir(outFolder):
        eggNOG_to_gff(eggNOG_dir,eggnog_gff)
    
if __name__ == '__main__':
	main()