#!/usr/bin/env python

import argparse
import sys
import subprocess
import time
import os
import yaml

def parse_config(config_file) :

    print "Loading configuration from " + str(config_file)
    config = open(config_file, 'r')
    return yaml.load(config)

def main():

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("-c", action='store', dest='config',
                        help="Configuration file.")
    args = parser.parse_args()

    if not args.config :
        parser.error('A configuration file needs to be specified.')

    config = parse_config(args.config)
   
    command = ['bash', '-c', 'source /nfs/slac/g/ldmx/software/setup.sh && env']
    proc = subprocess.Popen(command, stdout=subprocess.PIPE)

    for line in proc.stdout: 
        (key, _, value) = line.partition('=')
        os.environ[key] = value.strip()

    proc.communicate()

    detector = config['Detector'].strip()
    
    run_script = config['Script'].strip()
    
    path = config['Path'].strip()
    
    file_list = config['FileList'].strip()
    lhe_files = open(file_list, 'r')
    for lhe_path in lhe_files:

        command = 'python %s -l %s -d %s -p %s  ' % (run_script, lhe_path.strip(), detector, path)
        print command
        batch_command = "bsub -q medium -W 2800 %s" % command
        subprocess.Popen(batch_command, shell=True).wait()
        time.sleep(1)

if __name__ == "__main__" : 
    main()
    
