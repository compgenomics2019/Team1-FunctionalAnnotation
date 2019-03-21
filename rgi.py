#!/usr/bin/env python3
import argparse
import subprocess

def main():
    pars=argparse.ArgumentParser()
    pars.add_argument('-i_card_json',help='path to card.jason',required=True,type=str)
    pars.add_argument('-i_model',help='path to homology model',required=True,type=str)
    pars.add_argument('-i_main',help='path to fasta file',required=True,type=str)
    pars.add_argument('-o_prefix',help='ouput prefix',required=True,type=str)
    pars.add_argument('-t',help='read,contig,protein,wgs',required=True,type=str)
    args=pars.parse_args()
    card=args.i_card_json
    model=args.i_model
    main_input=args.i_main
    prefix=args.o_prefix
    t=args.t
    def rgi_function(card,model,main_input,prefix,t):
        subprocess.run(["rgi","load","-i",card,"--card_annotation",model,"--local"])
        subprocess.run(["rgi","main","-i",main_input,"-o",prefix,"--input_type",t,"--local"])
    rgi_function(card,model,main_input,prefix,t)
main()
    
    
