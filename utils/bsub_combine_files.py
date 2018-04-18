#!/usr/bin/python

import argparse
import sys
import ROOT as r
import os
import subprocess

from rootpy.io import root_open
from rootpy.io import DoesNotExist

def main() : 
   
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-d', action='store', dest='dir', 
                        help='Directory containing the list of files to crawl.')
    parser.add_argument('-s', action='store', dest='step_size', 
                        help='Number of files to merge together')
    parser.add_argument('-o', action='store', dest='output', 
                        help='Output directory')
    args = parser.parse_args()

    if not args.dir:
        parser.error('Please specify a path to the files to be processed.')

    if not args.output:
        parser.error('Please specify an output path.')

    step_size = 1
    if args.step_size: 
        step_size = int(args.step_size)

    # Get the list of all files and directories and filter out the directory
    # names. 
    files = [f for f in os.listdir(args.dir) if ".root" in f]
    print 'Processing %s files.' % len(files)
    
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    for i in range(0, len(files), step_size):

        input_files = "\'"
        for j in range(i, i+step_size, 1): 
            if j < len(files): input_files += " %s/%s" % (args.dir, files[j])
        input_files += "\'"

        command = "python combine_files.py -i %s -o %s" % (input_files, args.output)
        bsub_command = "bsub -q medium -W 2800 %s" % command
        subprocess.Popen(bsub_command, shell=True).wait()
        #subprocess.Popen(command, shell=True).wait()

if __name__ == "__main__": 
    main()


    

