import subprocess
import os
import sys
def main(tmhmm_gff,signalP_gff,piler_gff,card_gff,door2_gff,vfdb_gff,eggnog_gff,outDir):
    print("merging to one gff for each genome")
    #if outDir not in os.listdir():
    subprocess.call(['mkdir',outDir])
    eggnog_filesList=sorted(os.listdir(eggnog_gff))
    door2_filesList=sorted(os.listdir(door2_gff))
    tmhmm_fileList=sorted(os.listdir(tmhmm_gff))
    signalP_fileList=sorted(os.listdir(signalP_gff))
    card_fileList=sorted(os.listdir(card_gff))

    for i in range(50):
        eggnog=open('{}/{}'.format(eggnog_gff,eggnog_filesList[i]),"r")
        next(eggnog)
        eggnog=eggnog.readlines()
        door2=open('{}/{}'.format(door2_gff,door2_filesList[i]),"r")
        next(door2)
        door2=door2.readlines()
        #print(door2)
        tmhmmg=open('{}/{}'.format(tmhmm_gff,tmhmm_fileList[i]),"r",encoding='latin-1')
        next(tmhmmg)
        tmhmmg=tmhmmg.readlines()
        rgig=open('{}/{}'.format(card_gff,card_fileList[i]),"r")
        next(rgig)
        rgig=rgig.readlines()
        signalpg=open('{}/{}'.format(signalP_gff,signalP_fileList[i]),"r",encoding='latin-1')
        next(signalpg)
        signalpg=signalpg.readlines()
        egggff=[]
        for a in eggnog:
            a = a.strip("\n").split("\t")
            egggff.append(a)

        door = []
        for b in door2:
            b = b.strip("\n").split("\t")
            door.append(b)
        rgi = []
        for c in rgig:
            c = c.strip("\n").split("\t")
            rgi.append(c)
        tmhmm = []
        for d in tmhmmg:
            d=d.strip("\n").split("\t")
            tmhmm.append([d[0],d[1],d[5],d[3],d[4],d[6],d[7],d[8],d[2]])
        signalp = []
        for e in signalpg:
            e=e.strip("\n").split("\t")
            signalp.append([e[0],e[1],e[5],e[3],e[4],e[6],e[7],e[8],e[2]])
        gff=egggff+door+rgi+tmhmm+signalp


        output=open('{}/{}_faa.gff'.format(outDir,door2_filesList[i].split("_")[0]),"w+")
        output.write("##gff--version 3\n")
        for k in gff:
            output.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(k[0],k[1],k[2],k[3],k[4],k[5],k[6],k[7],k[8].replace(' ',';')))
        output.close()
    