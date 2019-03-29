# Team1 - Functional Annotation pipeline
This pipeline is designed by functional annotation team of group 1, to fully annotate biological functions of genes/proteins predicted from the results of gene prediction team. 
## Function Annotation Guidline
### Requirements
**1.** Python3  <br />
**2.** perl for TMHMM2.0 tool. The installed tool has perl path /usr/bin/perl. <br /> 
If the perl path is different from your local computer, please change it to /usr/bin/perl or make a symbolic link.  <br />
**3.** These tools are needed to be included in the current working directory with the FA_pipeline_final.py script, as in this git repo:
  * tmhmm-2.0c/bin/tmhmm
  * pilercr1.06/pilercr
  * signalp-5.0/bin/signalp
  * ncbi-blast-2.8.1+/bin containing blasts, blasts, makeblastdb
  * eggnog/eggnog-mapper/emapper.py 
  
**4.** These databases are also needed to be present in the current working directory, to run annotation for DOOR2 and VFDB:
  * operonDB.fasta
  * VFDBdb.fasta  <br />
**5.** Utilities folder, containing scripts to run with the FA_pipeline_final.py script  <br /> 
### Quick start
~~~~
Git clone https://github.gatech.edu/compgenomics2019/Team1-FunctionalAnnotation.git <br />
cd Team1-FunctionalAnnotation 
./FA_pipeline_final.py -p <path for .faa files> -n <path for .fna files> -a <path for .fasta files> -o <output name for final results> 
~~~~
#### Arguments
`-p `: directory that contains all the .faa files with known gene or RNA sequences from gene prediction <br />
`-a `: directory that contains all the .faa files with known protein sequences from gene prediction <br />
`-n`:a directory that contains all the .fasta files from assembly genome <br />
`-o`: name of folder that contains 50 off merged file 
### Output Description
In order to the final output specified by -o argument, there will be another two intermediate output generated after running the pipeline: <br />
  * output_annot: folder containing 50 output files from each annotation tool 
   * gff_all : folder containing 50 gff output from each annotation tool
When blast path is executed, it will also generate a database folder:
  * blast_operon_db: database for DOOR2
  * blast_vfdb_db: database for vfdb


