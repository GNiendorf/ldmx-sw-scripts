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
    
    jobs = int(config['Jobs'])
    print '[ BSUB ] Submitting %s jobs.' % jobs
   
    env_script = '/nfs/slac/g/ldmx/software/setup.sh'
    if 'EnvScript' in config: env_script = config['EnvScript'].strip()
    print '[ BSUB ] Environment script = %s' % env_script

    command = ['bash', '-c', 'source %s && env' % (env_script)]
    proc = subprocess.Popen(command, stdout=subprocess.PIPE)

    for line in proc.stdout: 
        (key, _, value) = line.partition('=')
        os.environ[key] = value.strip()

    proc.communicate()

    detector = config['Detector'].strip()

    run_script = config['Script'].strip()

    output_prefix = config['Output'].strip()

    path = config['Path'].strip()
    for job in xrange(0, jobs):
        output_path = "%s_%s" % (output_prefix, str(uuid.uuid4())[:8])
        log_path = output_path + ".log"
        print 'Log path: %s' % log_path

        command = 'python %s -d %s -p %s -o %s' % (run_script, detector, path, output_path)
        batch_command = "bsub -q medium -o %s -W 2800 %s" % (log_path,command)
        # batch_command = "bsub -q short -o %s -W 60 %s" % (log_path,command)
        #batch_command = command
        #print batch_command
        
        subprocess.Popen(batch_command, shell=True).wait()
        time.sleep(0.1)

if __name__ == "__main__" : 
    main()
    
