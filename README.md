# Team1 - Functional Annotation pipeline
This pipeline is designed by functional annotation team of group 1, to fully annotate biological functions of genes/proteins predicted from the results of gene prediction team. 
## Function Annotation Guidline
### Requirements
1. Python3
2. perl for TMHMM2.0 tool. The installed tool has perl path /usr/bin/perl. If the perl path is different from your local computer, please change it to /usr/bin/perl or make a symbolic link. 
3. These tools are needed to be included in the current working directory, as in this git repo:
* tmhmm-2.0c/bin/tmhmm
* pilercr1.06/pilercr
* signalp-5.0/bin/signalp
* ncbi-blast-2.8.1+/bin containing blasts, blasts, makeblastdb

### Quick start
.. `-p `: directory that contains all the .faa files with known gene or RNA sequences from gene prediction
`-a `: directory that contains all the .faa files with known protein sequences from gene prediction
`-n`:a directory that contains all the .fasta files from assembly genome
