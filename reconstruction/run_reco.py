#!/usr/bin/env python

import argparse
import os
import random
import sys
import subprocess
import time

def generate_macro(tpl, ifile, opath, scratch):
   
    config_path = '%s/config.py' % scratch
    f1 = open(tpl, 'r')
    f2 = open(config_path, 'w')
    base = os.path.splitext( os.path.basename(ifile) )[0]
    oname = '%s/reco_%s.root' % (opath,base)
    for line in f1:
        tmp1 = line.replace('$input', ifile);
        f2.write( tmp1.replace('$output', oname) )
    f1.close()
    f2.close()

    return config_path   

def main():

    parser = argparse.ArgumentParser(description='')
    parser.add_argument("-o", "--outputpath", help="Output file name.")
    parser.add_argument("-i", "--inputfile", help="Path to copy output to.")
    parser.add_argument("-c", "--configfile", help="Configuration template")
    args = parser.parse_args()


    # if not args.output:
    #     parser.error('Please specify an output file name.')
    
    #scratch_dir = '/nfs/slac/g/ldmx/scripts/tmp/%s' % os.environ['USER']
    scratch_dir = '/scratch/%s' % os.environ['USER']
    print 'Using scratch path %s' % scratch_dir
    if not os.path.exists(scratch_dir):
        os.makedirs(scratch_dir)
  
    tmp_dir = '%s/%s' % (scratch_dir, os.environ['LSB_JOBID'])
    #tmp_dir = '%s/%s' % (scratch_dir, 'test')
    print 'Creating tmp directory %s' % tmp_dir
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    
    os.system("cp cal_bdt.pkl %s/." % (tmp_dir) )
    os.chdir(tmp_dir)
   
    config_path = generate_macro(args.configfile,args.inputfile,args.outputpath,scratch_dir)
    subprocess.Popen(['ls', '.']).wait()
    command = "ldmx-app %s" % config_path
    subprocess.Popen(command, shell=True).wait()

    # prod_dir = args.outputpath
    # os.system('cp -r %s* %s' % (args.output, prod_dir))
    
    # os.system('rm -rf %s' % tmp_dir)
    # subprocess.Popen(['ls', scratch_dir]).wait()

if __name__ == "__main__" : 
    main()
