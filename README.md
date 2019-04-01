# Team1 - Functional Annotation pipeline
This pipeline is designed by functional annotation team of group 1, to fully annotate biological functions of genes/proteins predicted from the results of gene prediction team with ab initio and homology-based tools. <br />

Except for EggNOG, other functional tools take less than 15 mins, so we are going to run all 50 genomes with each tool.
For EggNOG, we used CD-HIT to cluster the .faa files, and run EGGNOG on the centroid file. From the EggNOG result, we
map to 50 genomes based on the cluster file generated by CD_HIT
After having all results annotated by different tools for each genomes, we merged all gffs into one gff file for each genome. <br />
## Function Annotation Guidline
### Requirements
**1.** python3 and python2 to run EggNOG annotation <br />

**2.** perl for TMHMM2.0 tool. The installed tool has perl path /usr/bin/perl. <br /> 

If the perl path is different from your local computer, please change it to /usr/bin/perl or make a symbolic link.  <br />

**3.** These tools are needed to be included in the current working directory with the FA_pipeline_final.py script, as in this git repo:
  * tmhmm-2.0c/bin/tmhmm
  * pilercr1.06/pilercr
  * signalp-5.0/bin/signalp
  * ncbi-blast-2.8.1+/bin containing blasts, blasts, makeblastdb
  * `eggnog-mapper` folder containing emapper.py. 
  
**4.** These databases are also needed to be present in the current working directory, to run annotation for DOOR2 and VFDB:
  * operonDB.fasta
  * VFDBdb.fasta 
  * `card-data` folder: a database to run `card` annotation 
  
**5.** `Utilities` folder, containing scripts to run with the FA_pipeline_final.py script <br /> 
**6.** `cd-hit` tool is installed or added to executable path. `cd-hit` can be installed with conda using the command:
  * `conda install -c bioconda cd-hit` or `conda install -c bioconda/label/cf201901 cd-hit` <br /> 
   Or user can download the source code of `cd-hit` following the instruction in this website: https://github.com/weizhongli/cdhit/wiki/2.-Installation <br /> 
**7.** `rgi` tool needs to be installed before running the pipeline. Users can install `rgi` source code at this website: https://github.com/arpcard/rgi. Or `rgi` can be installed using `conda`. For this pipeline, `rgi` version is 4.2.2. The command to install `rgi` is:
    * conda install -c conda-forge filetype

    * conda install -c conda-forge pyahocorasick

    * conda install -c conda-forge -c bioconda rgi=4.2.2

    * conda install -c biocore blast-plus <br />

### Quick start
~~~~
git clone https://github.gatech.edu/compgenomics2019/Team1-FunctionalAnnotation.git 
cd Team1-FunctionalAnnotation 
./FA_pipeline_final.py -p <path for .faa files> -n <path for .fna files> -a <path for .fasta files>  -oa<output name for annotation results> -og< output name for gff files> -om <output name for final results> 
OR
python3 FA_pipeline_final.py -p <path for .faa files> -n <path for .fna files> -a <path for .fasta files>  -oa<output name for annotation results> -og< output name for gff files> -om <output name for final results>
~~~~
#### Arguments
`-p `: directory that contains all the .faa files with known gene or RNA sequences from gene prediction <br />
`-a `: directory that contains all the .faa files with known protein sequences from gene prediction <br />
`-n`:a directory that contains all the .fasta files from assembly genome <br />
`-oa`: name of folder that contains annotation results<br />
`-og`: name of folder that contains converted gff results <br />
`-om`: name of folder that contains 50 off merged file 
### Output Description
- There will be a total of 3 output folders after executing the pipeline command. In addition to the final output specified by `-om` argument, there will be another two intermediate folders ,specified by `-oa` and `-og` arguments. The final output is a .gff file associated with each genome <br />
- In addition to the 3 output folders, there is another folder named `cluster-CDHIT`. This folder contains the centroid file, and another file describing cluster genes in each centroid. <br />
- When blast path is executed, it will also generate two database folders:
  * `blast_operon_db`: database for DOOR2
  * `blast_vfdb_db`: database for vfdb


