#!/usr/bin/env python
import os,sys
import optparse
import commands
import math
import time
import random
import fnmatch
from optparse import OptionParser

### options are at the bottom! 

def main(options,args): 

	idir = options.idir;
	listOfFiles = os.listdir(idir);
	listOfRootFiles = [];
	# for f in listOfFiles: 
	# 	if ".root" in f: listOfRootFiles.append( f );
	# print len(listOfRootFiles)

	listOfRootFiles = []
	for root, dirnames, filenames in os.walk(idir):
		for filename in fnmatch.filter(filenames, '*.root'): listOfRootFiles.append(os.path.join(root, filename))	

	# # make a submission directory, copy over necessary input files
	subdir = options.subdir; # subdir is where the output comes too
	swdir  = options.swdir;

	# njobs = options.njobs; 
	# eventsPerJob = options.eventsPerJob;
	# parEnergy = float(options.parEnergy);
	# parAngle  = float(options.parAngle);
	# parAngleConverted = math.tan(parAngle*math.pi/180);

	if not os.path.exists(subdir): os.makedirs(subdir)
	else:  
		os.system('rm -r %s' % subdir)
		os.makedirs(subdir)
	
	os.system('tar -cvzf inputs.tar.gz gammaMuAnalyzer.py tdrstyle.py');	
	os.system('mv inputs.tar.gz %s/.' % (subdir))
	os.chdir(subdir);

	print "number of reco files = ", len(listOfRootFiles);
	for i,fnf in enumerate(listOfRootFiles):

		fn = os.path.basename(fnf)
		path = os.path.split(fnf)[0]
		base = os.path.splitext(fn)[0]
		# print fn,path,base

		f1n = "tmp_%i_%s.sh" % (i,base);
		f1=open(f1n, 'w')
		f1.write('#!/bin/bash \n');
		f1.write('scl enable devtoolset-6 bash');
		# f1.write('source /u/ey/ntran/ldmx/setup/setup.sh \n');		
		f1.write('source %s/bin/ldmx-setup-env.sh \n' % (swdir));		
		f1.write('cp inputs.tar.gz ${__LSF_JOB_TMPDIR__}/. \n');
		f1.write('cp %s/%s ${__LSF_JOB_TMPDIR__}/. \n' % (path,fn));
		f1.write('cd ${__LSF_JOB_TMPDIR__} \n');
		f1.write('pwd \n');
		f1.write('tar -xvzf inputs.tar.gz \n');
		f1.write('ls -l \n');
		f1.write("python gammaMuAnalyzer.py -b -i %s -o ana_%s --tag %s \n" % (fn,fn,base));
		f1.write("mv *ana_%s ${LSB_OUTDIR}/. \n" % (fn));
		f1.close();

		command = 'bsub -q short -o olog_%s.log < tmp_%i_%s.sh' % (base,i,base);
		if not options.nosubmit: 
			os.system(command);
			time.sleep(0.1);

	# os.chdir("../.");

#----------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	
	parser = OptionParser()
	parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
	parser.add_option('-i','--idir', dest='idir'   , help='directory with reco data'        , default = 'data/')
	parser.add_option('--subdir'   , dest='subdir' , help='directory from which you submit' , default = 'tmp_ana')
	parser.add_option('--swdir'    , dest='swdir'  , help='release of ldmx-sw to use'       , default = '/nfs/slac/g/ldmx/software/ldmx-sw')
	parser.add_option('-S', '--no-submit'    ,    action="store_true"       ,  dest='nosubmit'           , help='Do not submit batch job.')

	(options, args) = parser.parse_args()

	main(options,args);
#----------------------------------------------------------------------------------------------------------------

