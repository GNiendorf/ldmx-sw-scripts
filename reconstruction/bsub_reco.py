#!/usr/bin/env python

import argparse
import os
import random
import sys
import subprocess
import time
import yaml
import uuid

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
   
    env_script = '/nfs/slac/g/ldmx/software/setup.sh'
    if 'EnvScript' in config: env_script = config['EnvScript'].strip()
    print '[ BSUB ] Environment script = %s' % env_script

    command = ['bash', '-c', 'source %s && env' % (env_script)]
    proc = subprocess.Popen(command, stdout=subprocess.PIPE)

    for line in proc.stdout: 
        (key, _, value) = line.partition('=')
        os.environ[key] = value.strip()

    proc.communicate()

    #detector = config['Detector'].strip()
    run_script = config['Script'].strip()
    config_tpl = config['RecoConfig'].strip()
    input_prefix = config['InputPath'].strip()
    output_prefix = config['OutputPath'].strip()

    if not os.path.exists(output_prefix):
        os.makedirs(output_prefix)

    files = [f for f in os.listdir(input_prefix) if ".root" in f]
    for i,f in enumerate(files): 
        
        input_file = "%s/%s" % (input_prefix,f)
        #log_path = '%s/reco_%s.log' % (output_prefix, f.split(".")[0])
        log_path = 'log_reco_%s.log' % (f.split(".")[0])
        command = 'python %s -o %s -c %s -i %s' % (run_script, output_prefix, config_tpl, input_file)
        batch_command = "bsub -q medium -o %s -W 2800 %s" % (log_path,command)
        # print command
        print batch_command

        subprocess.Popen(batch_command, shell=True).wait()
        time.sleep(0.1)

if __name__ == "__main__" : 
    main()
    
