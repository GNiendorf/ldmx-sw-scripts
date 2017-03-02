#!/usr/bin/env python
import os,sys
import optparse
import commands
import math
import random
from optparse import OptionParser

### options are at the bottom! 

def main(options,args): 

	# make a submission directory, copy over necessary input files
	subdir = options.subdir; # subdir is where the output comes too
	swdir  = options.swdir;
	xtag    = options.tag;

	njobs = options.njobs; 
	eventsPerJob = options.eventsPerJob;
	parEnergy = float(options.parEnergy);
	parAngle  = float(options.parAngle);
	parAngleConverted = math.tan(parAngle*math.pi/180);

	if not os.path.exists(subdir): os.makedirs(subdir)
	else:  
		os.system('rm -r %s' % subdir)
		os.makedirs(subdir)
	
	os.system('tar -cvzf inputs.tar.gz *.gdml *.dat *Config.py');	
	os.system('mv inputs.tar.gz %s/.' % (subdir))
	os.chdir(subdir);

	for i in range(njobs):
		
		# making the run script
		tag = "gun_job%s_energy%.2f_th%.2f_%s" % ( str(i),parEnergy,parAngle,xtag );

		f1n = "tmp_%s.sh" % (tag);
		f1=open(f1n, 'w')
		f1.write('#!/bin/bash \n');
		f1.write('source /u/ey/ntran/ldmx/setup/setup.sh \n');		
		f1.write('source %s/bin/ldmx-setup-env.sh \n' % (swdir));		
		f1.write('cp inputs.tar.gz tmp_%s.sh g4steer_%s.mac ${__LSF_JOB_TMPDIR__}/. \n' % (tag,tag));
		f1.write('cd ${__LSF_JOB_TMPDIR__} \n');
		f1.write('pwd \n');
		f1.write('tar -xvzf inputs.tar.gz \n');
		f1.write('ls -l \n');
		f1.write("ldmx-sim g4steer_%s.mac \n" % (tag));
		# f1.write("ldmx-app tmpRecoConfig.py \n");
		f1.write("mv ldmx_sim_events.root ${LSB_OUTDIR}/ldmx_sim_events_%s.root \n" % (tag));
		f1.close();

		# making the geant steering macro
		fsn = "g4steer_%s.mac" % tag;
		seed1 = 24345;
		seed2 = 35456;          		
		fs=open(fsn,'w');
		fs.write("/persistency/gdml/read detector.gdml \n");
		fs.write("/random/setSeeds %i %i \n" % (seed1+i, seed2+i));

		fs.write("/ldmx/biasing/enable \n");
		fs.write("/ldmx/biasing/particle gamma \n");
		fs.write("/ldmx/biasing/process GammaToMuPair \n");
		fs.write("/ldmx/biasing/volume target \n");
		fs.write("/ldmx/biasing/xsec 1000000000 \n");
		fs.write("/ldmx/biasing/threshold 1600 \n");

		fs.write("/ldmx/plugins/load TargetBremFilter libBiasing.so \n");
		fs.write("/ldmx/plugins/load TargetProcessFilter libBiasing.so \n");

		fs.write("/run/initialize \n");

		fs.write("/gun/particle e- \n");
		fs.write("/gun/energy %.2f GeV \n" % (parEnergy));
		fs.write("/gun/position 0 0 -1 mm \n");
		fs.write("/gun/direction %.2f 0.0 1.0 \n" % (parAngleConverted));
		fs.write("/run/beamOn %i \n" % (eventsPerJob));
		fs.close();

		command = 'bsub -W 2800 -q long -o olog_%s.log < tmp_%s.sh' % (tag,tag);
		if not options.nosubmit: os.system(command);

	os.chdir("../.");

#----------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	
	parser = OptionParser()
	parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
	parser.add_option("--lumi", dest="lumi", type=float, default = 30,help="luminosity", metavar="lumi")
	parser.add_option('-i','--idir', dest='idir', default = 'data/',help='directory with data', metavar='idir')
	parser.add_option('-o','--odir', dest='odir', default = 'plots/',help='directory to write plots', metavar='odir')
	parser.add_option('--subdir'            ,    dest='subdir'             , help='directory from which you submit' , default='tmp_condor')
	parser.add_option('--swdir'            ,    dest='swdir'             , help='directory from which you submit' , default='/uscms_data/d2/ntran/physics/LDMX/FullFramework/go9/ldmx-sw')

	parser.add_option('--tag'                ,    dest='tag'             , help='directory from which you submit' , default='det1')
	parser.add_option('--parEnergy'          ,    dest='parEnergy'             , help='directory from which you submit' , default=3.)
	parser.add_option('--parAngle'          ,    dest='parAngle'             , help='directory from which you submit' , default=0.)
	parser.add_option('-N', '--njobs'        ,    dest='njobs'              , help='number of jobs'           , default=1, type=int)
	parser.add_option('-E', '--eventsPerJob' ,    dest='eventsPerJob'              , help='number of events per job'           , default=100, type=int)
	parser.add_option('-S', '--no-submit'    ,    action="store_true"       ,  dest='nosubmit'           , help='Do not submit batch job.')

	(options, args) = parser.parse_args()

	main(options,args);
#----------------------------------------------------------------------------------------------------------------

