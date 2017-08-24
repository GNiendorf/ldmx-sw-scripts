#!/usr/bin/env python

import argparse
import os
import random
import sys
import subprocess
import time

def generate_macro(lhe_path, output_path):
    print "Processing file %s" % lhe_path
    
    macro_path = output_path + ".mac"
    print 'Writing macro to %s' % macro_path
    macro_file = open(macro_path, 'w')
    macro_file.write('/persistency/gdml/read detector.gdml\n')
    macro_file.write('/ldmx/pw/enable\n')
    macro_file.write('/ldmx/pw/read detectors/scoring_planes/detector.gdml\n')
    macro_file.write('/run/initialize\n')
    macro_file.write('/ldmx/generators/beamspot/enable\n')
    macro_file.write('/ldmx/generators/beamspot/sizeX 20*mm\n')
    macro_file.write('/ldmx/generators/beamspot/sizeY 40*mm\n')
    macro_file.write('/ldmx/generators/beamspot/sizeZ .3504*mm\n')
    macro_file.write('/ldmx/plugins/load EventPrintPlugin\n')
    macro_file.write('/ldmx/plugins/EventPrintPlugin/modulus 500\n')
    macro_file.write('/ldmx/persistency/root/verbose 1\n')
    macro_file.write('/ldmx/persistency/root/file ' + output_path + '.root\n')
    macro_file.write('/ldmx/generators/lhe/open ' + lhe_path + '\n')
    macro_file.write('/run/beamOn 10000000\n') 
    macro_file.close()

    return macro_path    

def main():

    parser = argparse.ArgumentParser(description='')
    parser.add_argument("-l", "--lhe", help="LHE files to process")
    parser.add_argument("-d", "--detector", help="Detector name.")
    parser.add_argument("-p", "--path", help="Path to copy output to.")
    args = parser.parse_args()

    if not args.lhe:
        parser.error('Please specify an LHE file to process.')

    #scratch_dir = '/nfs/slac/g/ldmx/production/scripts/tmp/%s' % os.environ['USER']
    scratch_dir = '/scratch/%s' % os.environ['USER']
    print 'Using scratch path %s' % scratch_dir
    if not os.path.exists(scratch_dir):
        os.makedirs(scratch_dir)

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

    output_path = args.lhe.strip()[:-4]
    output_path = output_path[output_path.rfind('/') + 1:]

    macro_path = generate_macro(args.lhe.strip(), output_path) 
    command = "ldmx-sim %s" % macro_path
    subprocess.Popen(command, shell=True).wait()
    
    os.rename('currentEvent.rndm', output_path + '_Event.rndm')
    os.rename('currentRun.rndm', output_path + '_Run.rndm')
     
    prod_dir = args.path
    os.system('cp -r %s* %s' % (output_path, prod_dir))
    
    os.system('rm -rf %s' % tmp_dir)
    subprocess.Popen(['ls', scratch_dir]).wait()
    
if __name__ == "__main__" : 
    main()
