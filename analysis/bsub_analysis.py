#!/usr/bin/env python
import os,sys
import optparse
import commands
import math
import time
import random
import fnmatch
import yaml
import argparse

from optparse import OptionParser

def parse_config(config_file) :

	print "Loading configuration from " + str(config_file)
	config = open(config_file, 'r')
	return yaml.load(config)

def main(): 

	# Parse command line arguments
	parser = argparse.ArgumentParser(description='')
	parser.add_argument("-c", action='store', dest='config',help="Configuration file.")
	args = parser.parse_args()
	if not args.config : parser.error('A configuration file needs to be specified.')
	config = parse_config(args.config)

	idir      = config['InputPath'].strip()
	subdir    = config['OutputPath'].strip()
	envscript = config['EnvScript'].strip()
	analyzer  = config['Analyzer'].strip()

	if not os.path.exists(subdir): os.makedirs(subdir)
	# else:  
	# 	os.system('rm -r %s' % subdir)
	# 	os.makedirs(subdir)	

	listOfRootFiles = []
	for root, dirnames, filenames in os.walk(idir):
		for filename in fnmatch.filter(filenames, '*.root'): listOfRootFiles.append(os.path.join(root, filename))	
	
	os.system('tar -cvzf inputs.tar.gz gammaMuAnalyzer.py tdrstyle.py');	
	os.system('mv inputs.tar.gz %s/.' % (subdir))
	os.chdir(subdir);

	print "number of reco files = ", len(listOfRootFiles);
	for i,fnf in enumerate(listOfRootFiles):

		fn = os.path.basename(fnf)
		path = os.path.split(fnf)[0]
		base = os.path.splitext(fn)[0]
		# print i,fn,path,base

		f1n = "tmp_%i_%s.sh" % (i,base);
		f1=open(f1n, 'w')
		f1.write('#!/bin/bash \n');
		f1.write('scl enable devtoolset-6 bash \n');
		# f1.write('source /u/ey/ntran/ldmx/setup/setup.sh \n');		
		f1.write('source %s \n' % (envscript));		
		f1.write('cp inputs.tar.gz ${__LSF_JOB_TMPDIR__}/. \n');
		f1.write('cp %s/%s ${__LSF_JOB_TMPDIR__}/. \n' % (path,fn));
		f1.write('cd ${__LSF_JOB_TMPDIR__} \n');
		f1.write('pwd \n');
		f1.write('tar -xvzf inputs.tar.gz \n');
		f1.write('ls -l \n');
		f1.write("python %s -b -i %s -o ana_%s --tag %s \n" % (analyzer,fn,fn,str(i)));
		f1.write("mv *ana_%s ${LSB_OUTDIR}/. \n" % (fn));
		f1.close();

		#print ("hist_ana_%s" % (fn));
		command = 'bsub -q short -o olog_%s.log < tmp_%i_%s.sh' % (base,i,base);
		fileExists = False;
		if (os.path.isfile("hist_ana_%s" % (fn))): fileExists = True; #print "file already exists!"
		if not fileExists:
			print "file %i does not exists, submit job..." % (i)
			os.system(command);
			time.sleep(0.1);
		# if i > 5: break;
		
	# os.chdir("../.");

#----------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	main();
#----------------------------------------------------------------------------------------------------------------

