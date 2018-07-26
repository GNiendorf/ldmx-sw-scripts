#!/usr/bin/env python

import argparse
import os
import random
import sys
import subprocess
import time

def generate_macro(output_path):
   
    random.seed(time.time())
    seed1 = int(random.random()*100000)
    seed2 = int(random.random()*100000)

    macro_path = output_path + ".mac"
    print 'Writing macro to %s' % macro_path
    macro_file = open(macro_path, 'w')
    macro_file.write('/persistency/gdml/read detector.gdml\n')
    macro_file.write('/ldmx/pw/enable \n')
    macro_file.write('/ldmx/pw/read detectors/scoring_planes/detector.gdml\n')

    # photon biasing
    macro_file.write("/ldmx/biasing/enable \n");
    macro_file.write("/ldmx/biasing/particle gamma \n");
    macro_file.write("/ldmx/biasing/process GammaToMuPair \n");
    macro_file.write("/ldmx/biasing/volume target \n");
    macro_file.write("/ldmx/biasing/threshold 2500 \n");

    # initialize
    macro_file.write('/run/initialize\n')

    # ?? redundant ??
    macro_file.write('/ldmx/biasing/xsec/particle gamma\n')
    macro_file.write('/ldmx/biasing/xsec/process GammaToMuPair\n')
    macro_file.write('/ldmx/biasing/xsec/threshold 2500\n')
    macro_file.write('/ldmx/biasing/xsec/factor 1000000000\n')    

    # particle gun
    macro_file.write('/gun/particle e-\n')
    macro_file.write('/gun/energy 4.0 GeV\n')
    macro_file.write('/gun/position 0. 0. -.55 mm\n')
    macro_file.write('/gun/direction 0. 0. 4.0 GeV\n')    

    macro_file.write('/ldmx/plugins/load EventPrintPlugin\n')
    macro_file.write('/ldmx/plugins/EventPrintPlugin/modulus 10000\n')

    # target filter
    macro_file.write('/ldmx/plugins/load TargetBremFilter libBiasing.so\n')
    macro_file.write('/ldmx/plugins/TargetBremFilter/volume target_PV\n')
    macro_file.write('/ldmx/plugins/TargetBremFilter/recoil_threshold 1500\n')
    macro_file.write('/ldmx/plugins/TargetBremFilter/brem_threshold 2500\n')

    # beamspot
    macro_file.write('/ldmx/generators/beamspot/enable\n')
    macro_file.write('/ldmx/generators/beamspot/sizeX 20.0\n')
    macro_file.write('/ldmx/generators/beamspot/sizeY 40.0\n')
    
    # pruning output
    macro_file.write('/ldmx/persistency/root/dropCol MagnetScoringPlaneHits\n')
    macro_file.write('/ldmx/persistency/root/dropCol TrackerScoringPlaneHits\n')
    macro_file.write('/ldmx/persistency/root/dropCol HcalScoringPlaneHits\n')
    macro_file.write('/ldmx/persistency/root/dropCol TargetScoringPlaneHits\n')
    macro_file.write('/ldmx/persistency/root/verbose 1\n')
    macro_file.write('/ldmx/persistency/root/file ' + output_path + '.root\n')
    macro_file.write('/random/setSeeds %s %s\n' % (seed1, seed2)) 
    macro_file.write('/run/beamOn 2000000\n') 
    # macro_file.write('/run/beamOn 1000\n') 
    macro_file.close()

    return macro_path   

def main():

    parser = argparse.ArgumentParser(description='')
    parser.add_argument("-e", "--envscript", help="env script.")
    parser.add_argument("-o", "--output", help="Output file name.")
    parser.add_argument("-d", "--detector", help="Detector name.")
    parser.add_argument("-p", "--path", help="Path to copy output to.")
    parser.add_argument("-l", "--ldmxswpath", help="Path to copy output to.")
    args = parser.parse_args()


    if not args.output:
        parser.error('Please specify an output file name.')

    env_command = ['bash', '-c', 'source %s && env' % args.envscript]
    subprocess.Popen(env_command, stdout=subprocess.PIPE)
    
    #scratch_dir = '/nfs/slac/g/ldmx/scripts/tmp/%s' % os.environ['USER']
    scratch_dir = '/scratch/%s' % os.environ['USER']
    print 'Using scratch path %s' % scratch_dir
    if not os.path.exists(scratch_dir):
        os.makedirs(scratch_dir)

    os.system("which ldmx-sim");
  
    tmp_dir = '%s/%s' % (scratch_dir, os.environ['LSB_JOBID'])
    #tmp_dir = '%s/%s' % (scratch_dir, 'test')
    print 'Creating tmp directory %s' % tmp_dir
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    
    os.chdir(tmp_dir)

    detector = args.detector.strip()
    detector_path = '/nfs/slac/g/ldmx/software/ldmx-sw/Detectors/data'
    detector_path += '/%s' % detector
    print 'Path to detector: %s' % detector_path
    os.system('ln -s %s/* .' % detector_path)
    os.symlink('/nfs/slac/g/ldmx/software/ldmx-sw/Detectors/data', 'detectors')
    os.symlink('/nfs/slac/g/ldmx/software/fieldmap/BmapCorrected3D_13k_unfolded_scaled_1.15384615385.dat', 'BmapCorrected3D_13k_unfolded_scaled_1.15384615385.dat')
   
    macro_path = generate_macro(args.output)
    subprocess.Popen(['ls', '.']).wait()
    command = "ldmx-sim %s" % macro_path
    subprocess.Popen(command, shell=True).wait()
    
    os.rename('currentEvent.rndm', args.output + '_Event.rndm')
    os.rename('currentRun.rndm', args.output + '_Run.rndm')
    subprocess.Popen(['ls', tmp_dir]).wait()

    prod_dir = args.path
    os.system('cp -r %s* %s' % (args.output, prod_dir))
    
    os.system('rm -rf %s' % tmp_dir)
    subprocess.Popen(['ls', scratch_dir]).wait()

if __name__ == "__main__" : 
    main()
