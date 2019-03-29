# Team1 - Functional Annotation pipeline
This pipeline is designed by functional annotation team of group 1, to fully annotate biological functions of genes/proteins predicted from the results of gene prediction team. 
## Function Annotation Guidline
### Requirements
1. Python3
2. perl for TMHMM2.0 tool. The installed tool has perl path /usr/bin/perl. <br /> If the perl path is different from your local computer, please change it to /usr/bin/perl or make a symbolic link. 
3. These tools are needed to be included in the current working directory with the FA_pipeline_final.py script, as in this git repo:
 * tmhmm-2.0c/bin/tmhmm
 * pilercr1.06/pilercr
 * signalp-5.0/bin/signalp
 * ncbi-blast-2.8.1+/bin containing blasts, blasts, makeblastdb
 * eggnog-mapper/emapper.py
4. These databases are also needed to be present in the current working directory, to run annotation for DOOR2 and VFDB:
 * operonDB.fasta
 * VFDBdb.fasta

### Quick start
`Git clone https://github.gatech.edu/compgenomics2019/Team1-FunctionalAnnotation.git ` <br />
`cd Team1-FunctionalAnnotation` <br />
`./FA_pipeline_final.py -p <path for .faa files> -n <path for .fna files> -a <path for .fasta files> -o <output name for final results> <br />` <br />
#### Arguments
`-p `: directory that contains all the .faa files with known gene or RNA sequences from gene prediction <br />
`-a `: directory that contains all the .faa files with known protein sequences from gene prediction <br />
`-n`:a directory that contains all the .fasta files from assembly genome <br />
`-o`: name of folder that contains 50 off merged file 
