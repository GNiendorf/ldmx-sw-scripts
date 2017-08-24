
# Don't email batch job log
export LSB_JOB_REPORT_MAIL=N

export SOFTWARE_HOME=/nfs/slac/g/ldmx/software
export LDMXSW_HOME=/u/ey/ntran/ldmx/dev/muons/officialv3

################
#   Anaconda   #
################
export ANACONDA_HOME=$SOFTWARE_HOME/anaconda
export PATH=$ANACONDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$ANACONDA_HOME/lib:$LD_LIBRARY_PATH

###########
#   GCC   #
###########
export CXX=$ANACONDA_HOME/bin/g++
export CC=$ANACONDA_HOME/bin/gcc

##############
#   Xerces   #
##############
export XercesC_DIR=$SOFTWARE_HOME/xerces
export LD_LIBRARY_PATH=$XercesC_DIR/lib:$LD_LIBRARY_PATH

# fix for Natalia's Geant
export G4DIR=/nfs/slac/g/ldmx/users/ntoro/geant4-muons/geant4.10.02.p02-install
source $G4DIR/bin/geant4.sh

############
#   ROOT   #
############
export ROOTDIR=$SOFTWARE_HOME/root/rbuild
source $ROOTDIR/bin/thisroot.sh

###############
#   ldmx-sw   #
###############
export PATH=$LDMXSW_HOME/ldmx-sw/install/bin:$PATH
export LD_LIBRARY_PATH=$LDMXSW_HOME/ldmx-sw/install/lib:$LD_LIBRARY_PATH
