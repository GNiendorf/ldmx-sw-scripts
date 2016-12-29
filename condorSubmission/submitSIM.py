#!/usr/bin/env python
import os,sys
import optparse
import commands
import math
import random
from optparse import OptionParser

### options are at the bottom! 

def main(options,args): 

	subdir = options.subdir;
	swdir  = options.swdir;
	odir   = options.odir;

	if not os.path.exists(subdir): os.makedirs(subdir)
	else:  
		os.system('rm -r %s' % subdir)
		os.makedirs(subdir)
	
	njobs = options.njobs; 

	os.system("cp /uscms_data/d2/ntran/physics/LDMX/FullFramework/go12/ldmx-sw/go1/*.gdml /uscms_data/d2/ntran/physics/LDMX/FullFramework/go12/ldmx-sw/go1/*.dat setupLPC.sh %s/." % (subdir))
	os.chdir(subdir);
	os.system("tar -cvzf inputs.tar.gz setupLPC.sh *.gdml *.dat" );

	for i in range(njobs):

		tag = "gun_job%s" % ( str(i) );

		# making the run script
		f1n = "tmp_%s.sh" % (tag);
		f1=open(f1n, 'w')
		f1.write('#!/bin/bash \n');
		f1.write("tar -xvzf inputs.tar.gz \n");		
		f1.write("sed 's|REPLACEME|%s|' < setupLPC.sh > setupLPC-new.sh \n" % (swdir));		
		f1.write("source setupLPC-new.sh \n");
		f1.write("ls \n");
		f1.write("ldmx-sim g4steer_%s.mac \n" % (tag));
		f1.write("xrdcp ldmx_sim_events.root root://cmseos.fnal.gov/%s/ldmx_sim_events_%s.root \n" % (odir,tag));
		f1.write("ldmx-hcal-digi-producer ldmx_sim_events.root ldmx_hcal_digi.root \n");
		f1.write("xrdcp ldmx_hcal_digi.root root://cmseos.fnal.gov/%s/ldmx_hcal_digi_%s.root \n" % (odir,tag));		
		f1.write("rm ldmx_sim_events.root ldmx_hcal_digi.root \n");		
		f1.close();

		# making the geant steering macro
		fsn = "g4steer_%s.mac" % tag;
		fs=open(fsn,'w');
		fs.write("/persistency/gdml/read detector-hcalOnly.gdml \n");
		fs.write("/random/setSeeds 12354 23465 \n");
		fs.write("/run/initialize \n");
		fs.write("/gun/particle neutron \n");
		fs.write("/gun/energy 3 GeV \n");
		fs.write("/gun/position 0 0 200 mm \n");
		fs.write("/gun/direction 0.0 0.0 1.0 GeV \n");
		fs.write("/run/beamOn 100 \n");
		fs.close();

		# making the jdl file
		f2n = "tmp_%s.jdl" % (tag);
		outtag = "out_%s_$(Cluster)" % (tag)
		f2=open(f2n, 'w')
		f2.write("universe = vanilla \n");
		f2.write("Executable = %s \n" % (f1n) );
		f2.write('Requirements = OpSys == "LINUX" && (Arch != "DUMMY" )\n');
		f2.write("request_disk = 10000000\n");
		f2.write("request_memory = 2100\n");
		f2.write("Should_Transfer_Files = YES \n");
		f2.write("Transfer_Input_Files = inputs.tar.gz,g4steer_%s.mac \n" % (tag));
		f2.write("WhenToTransferOutput  = ON_EXIT_OR_EVICT \n");
		f2.write("Output = "+outtag+".stdout \n");
		f2.write("Error = "+outtag+".stderr \n");
		f2.write("Log = "+outtag+".log \n");
		f2.write("Notification    = Error \n");
		f2.write("x509userproxy = $ENV(X509_USER_PROXY) \n")
		f2.write("Queue 1 \n");
		f2.close();

		if not options.nosubmit: os.system("condor_submit %s" % (f2n));

	########## end of loop
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
	parser.add_option('-N', '--njobs'       ,    dest='njobs'              , help='number of jobs'           , default=1, type=int)
	parser.add_option('-S', '--no-submit'   ,    action="store_true"       ,  dest='nosubmit'           , help='Do not submit batch job.')

	(options, args) = parser.parse_args()

	main(options,args);
#----------------------------------------------------------------------------------------------------------------

