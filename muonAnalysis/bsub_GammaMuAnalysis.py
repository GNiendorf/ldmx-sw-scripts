#!/usr/bin/env python
import os,sys
import optparse
import commands
import math
import random
from optparse import OptionParser

### options are at the bottom! 

def main(options,args): 

	idir = options.idir;
	listOfFiles = os.listdir(idir);
	listOfRootFiles = [];
	for f in listOfFiles: 
		if ".root" in f: listOfRootFiles.append( f );
	print len(listOfRootFiles)

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
	
	os.system('tar -cvzf inputs.tar.gz gammaMuAnalyzer.py tdrstyle.py Loader.C');	
	os.system('mv inputs.tar.gz %s/.' % (subdir))
	os.chdir(subdir);

	for i,fnf in enumerate(listOfRootFiles):

		fn = os.path.splitext(fnf)[0] 
		print i,fn

		f1n = "tmp_%i_%s.sh" % (i,fn);
		f1=open(f1n, 'w')
		f1.write('#!/bin/bash \n');
		f1.write('source /u/ey/ntran/ldmx/setup/setup.sh \n');		
		f1.write('source %s/bin/ldmx-setup-env.sh \n' % (swdir));		
		f1.write('cp inputs.tar.gz ${__LSF_JOB_TMPDIR__}/. \n');
		f1.write('cp %s/%s.root ${__LSF_JOB_TMPDIR__}/. \n' % (options.idir,fn));
		f1.write('cd ${__LSF_JOB_TMPDIR__} \n');
		f1.write('pwd \n');
		f1.write('tar -xvzf inputs.tar.gz \n');
		f1.write('ls -l \n');
		f1.write("python gammaMuAnalyzer.py -b -i %s.root -o ana_%s.root --tag %i \n" % (fn,fn,i));
		f1.write("mv ana_%s.root ${LSB_OUTDIR}/ana_%i_%s.root \n" % (fn,i,fn));
		f1.close();

		command = 'bsub -q short -o olog_%s.log < tmp_%i_%s.sh' % (fn,i,fn);
		if not options.nosubmit: os.system(command);

	# os.chdir("../.");

#----------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	
	parser = OptionParser()
	parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
	# parser.add_option("--lumi", dest="lumi", type=float, default = 30,help="luminosity", metavar="lumi")
	parser.add_option('-i','--idir', dest='idir', default = 'data/',help='directory with data', metavar='idir')
	# parser.add_option('-o','--odir', dest='odir', default = 'plots/',help='directory to write plots', metavar='odir')
	parser.add_option('--subdir'            ,    dest='subdir'             , help='directory from which you submit' , default='tmp_condor')
	parser.add_option('--swdir'            ,    dest='swdir'             , help='directory from which you submit' , default='/uscms_data/d2/ntran/physics/LDMX/FullFramework/go9/ldmx-sw')
	parser.add_option('-S', '--no-submit'    ,    action="store_true"       ,  dest='nosubmit'           , help='Do not submit batch job.')

	(options, args) = parser.parse_args()

	main(options,args);
#----------------------------------------------------------------------------------------------------------------

