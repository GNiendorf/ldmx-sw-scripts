#!/usr/bin/python

import argparse
import sys
import ROOT as r
import os
import subprocess
import random

def main(): 

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', action='store', dest='input', 
                        help='List of input files to merge.')
    parser.add_argument('-o', action='store', dest='output', 
                        help='Output directory')
    args = parser.parse_args()

    input_files = args.input
    file_list = input_files.split()

    base = os.path.splitext( os.path.basename(file_list[1]) )[0]
    base += '_merge.root'

    scratch_dir = '/scratch/%s' % os.environ['USER']
    
    tmp_dir = '%s/%s' % (scratch_dir, os.environ['LSB_JOBID'])
    #tmp_dir = '%s/test_dir_%s' % (scratch_dir, random.randrange(0, 101, 2))
    print 'Creating tmp directory %s' % tmp_dir
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    
    os.chdir(tmp_dir)
    
    for ifile in file_list: 
        os.system('cp %s .' % ifile)

    command = "hadd -f %s *.root" % base
    subprocess.Popen(command, shell=True).wait()

    os.system('cp %s %s' % (base, args.output))
    os.chdir('../')
    os.system('rm -rf %s' % tmp_dir)

if __name__ == "__main__": 
    main()
