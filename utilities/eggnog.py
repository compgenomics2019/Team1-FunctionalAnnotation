#!/usr/bin/python2
import subprocess
import os
import sys
""" because eggnog use python2. I have to create seperate files to call eggnog function """


print("Annotating cluster file with eggNOG.")
outFolder=sys.argv[1]
if os.path.exists(outFolder):
	print(outFolder)
	subprocess.call(["rm","-dr",outFolder])
subprocess.call(["mkdir", outFolder])
#subprocess.call(["mkdir", "eggnog_result"])
""" subprocess.call(["python2", "../installed_tools/eggnog-mapper/emapper.py",
				"-i", "cluster_CDHIT/clusterFile.txt", 
				"-o", os.path.join(outFolder,"eggnogOutput"),
				"-m", "hmmer",
				"-d", "bact",
				"--cpu", "04",
				"--usemem"]) """
subprocess.call(["python2", "eggnog-mapper/emapper.py",
				"-i", "cluster_CDHIT/clusterFile.txt", 
				"-o", os.path.join(outFolder,"eggnogOutput"),
				"-m", "hmmer",
				"-d", "bact",
				"--cpu", "04",
				"--usemem"])
