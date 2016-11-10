#!/bin/bash

swdir="/uscms_data/d2/awhitbe1/workArea/LDMX"
ldmxdir="REPLACEME"

export PATH=$ldmxdir/ldmx-sw-install/bin:$swdir/cmake-3.6.2-Linux-x86_64/bin/:/cvmfs/cms.cern.ch/slc6_amd64_gcc481/external/gcc/4.8.1/bin:$PATH
export G4DIR=$swdir/geant4.10.02.p02-install
export ROOTDIR=$swdir/root-6.06.08-build
export Geant4_DIR=$swdir/geant4.10.02.p02/build
export LD_LIBRARY_PATH=$ldmxdir/ldmx-sw-install/lib:$swdir/xerces-c-3.1.4/lib:$swdir/root-6.06.08-build/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc481/external/gcc/4.8.1/lib64:/cvmfs/cms.cern.ch/slc6_amd64_gcc481/external/gcc/4.8.1/lib:$LD_LIBRARY_PATH

# set this up beforehand because whatever is in ldmx-setup-env.sh is broken
source /uscms_data/d2/awhitbe1/workArea/LDMX/geant4.10.02.p02-install/bin/geant4.sh
source /uscms_data/d2/awhitbe1/workArea/LDMX/root-6.06.08-build/bin/thisroot.sh

