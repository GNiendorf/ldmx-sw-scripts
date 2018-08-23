#!/usr/bin/env python

"""
file: cosmic_muon_lhe_generator.py
author: Reese Petersen
affiliations: University of Minnesota, LDMX Collaboration
email: pet00831@umn.edu
date: 16 July 2018
description: This script writes lhe files which descibe cosmic muons 
with energy and momentum distributed according to a function provided by
A. Dar in "Atmospheric Neutrinos, Astrophysical Neutrons, and Proton-Decay Experiments",
18 July, 1983, Phys. Rev. Lett. Vol 51, No. 3, pg 227
Other papers necessary to understand this function in its entirety include reference 7 from A. Dar:
"The Muon Charge Ratio at Sea-Level" by A. Liland, 
16th International Cosmic Ray Conference, 
Conference Papers vol. 13 (Late Papers), Kyoto, Japan, August 1979

example usage: ./cosmic_muon_lhe_generator.py --numEvents 1000 

"""

import os
import argparse
import math
import random
import ROOT

# defaults
numEvents_d = 10
numFiles_d = 1
outputDir_d = ""
emin_d = 1.
emax_d = 100.
thmin_d = 0.
thmax_d = 75.
ebins = 100
thbins = 100
geometry_d = "v9"
# get number of events
parser = argparse.ArgumentParser(description = "Makes lhe files for cosmic muons intersecting the HCal of the LDMX detector.")
parser.add_argument("--numEvents" , dest = "numEvents" , help = "number of events per lhe file, default = %s"%(numEvents_d)                        , default = numEvents_d, type = int)
parser.add_argument("--numFiles"  , dest = "numFiles"  , help = "number of lhe files to make, default = %s"%(numFiles_d)                           , default = numFiles_d, type = int)
parser.add_argument("--outputDir" , dest = "outputDir" , help = "the directory to put the cmmc lhe files, default = %s"%(outputDir_d)              , default = outputDir_d)
parser.add_argument("--energyMin" , dest = "energyMin" , help = "The low energy limit for the muon spectrum in GeV, default = %f"%(emin_d)         , default=emin_d)
parser.add_argument("--energyMax" , dest = "energyMax" , help = "The high energy limit for the muon spectrum in GeV, default = %f"%(emax_d)        , default=emax_d)
parser.add_argument("--thetaMin"  , dest = "thetaMin"  , help = "The low theta limit for the muon specturm in degrees, default = %f"%(thmin_d)     , default=thmin_d)
parser.add_argument("--thetaMax"  , dest = "thetaMax"  , help = "The high theta limit for the muon spectrum in degrees, default = %f"%(thmax_d)    , default=thmax_d)
parser.add_argument("--geometry"  , dest = "geometry"  , help = "The detector geometry (v3 through v10 available), default = %s"%(geometry_d)      , default=geometry_d)
arg = parser.parse_args()

ROOT.gRandom.SetSeed(0)
# strip trailing slash and make the output directory if it does not exist
output = arg.outputDir
if output != "":
  if len(output.split('/')) != 2:
    output = output+"/"
  if not os.path.exists(output):
    print "cosmic_muon_lhe_generator.py: Outpath does not exist, making %s"%(output)
    os.makedirs(output)
# inputs to generate the muons
emin = float(arg.energyMin)
emax = float(arg.energyMax)
thmin = float(arg.thetaMin)
thmax = float(arg.thetaMax)
# muon mass in GeV
m = 0.1056583715
# ADar is the muon differential flux as a function of energy (in GeV) and zenith angle (in degrees) given by A. Dar (Eq. 6) in 
# "Atmospheric Neutrinos, Astrophysical Neutrons, and Proton-Decay Experiments", 18 July, 1983, Phys. Rev. Lett. Vol 51, No. 3, pg 227
# The original function has units of muons/GeV/sr/s/cm^2, ADarplus and ADarminus are still expressed in these units, ADar has been normalized to 1 over the default range.
# This spectrum is fit to data taken at DESY, Hamburg, Germany (53.58 deg N, 9.88 deg E) at 0 degrees and 75 degrees in zenith angle at approximately sea-level altitude. (40 m)
# This spectrum matches data in the range: E = 0.3-1000 GeV, th = 0-75 GeV
# Effects from the environment of the detector, such as the building it will be housed in, have not been considered.
# The East-West charge ratio has not been accounted for. There is no azimuthal angular dependence. In other words, Earth's magnetic field has not been accounted for.
# The East-West charge ratio would have very little effect for muons with energy > 10 GeV and zenith angle < 75 degrees.
# The muon spectrum has two parts, one for positive muons, and one for negative muons.
# ADar is used to simulate the energy and zenith angle of an incoming cosmic muon, ADar = ADarplus + ADarminus normalized to 1 over the default range (1-100 GeV, 0-75 degrees)
# ADarplus and ADarminus, which are the separate spectra for positive and negative muons, are used to determine the charge of each cosmic muon after the energy and angle are generated.
ADar = "(0.3403105255419549*TMath::Exp(2.172701227027019/(-1.0609+0.1236*TMath::Cos(TMath::Pi()/180*y)-x*TMath::Cos(TMath::Pi()/180*y)))*TMath::Power(TMath::Cos(TMath::Pi()/180*y),2.67-1.0106422229299041/(-1.0609+0.1236*TMath::Cos(TMath::Pi()/180*y)-x*TMath::Cos(TMath::Pi()/180*y)))*(-0.09553777560317707*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))+6.68495653879148e-9*TMath::Power(TMath::Cos(TMath::Pi()/180*y),3.5)+TMath::Sqrt(2.1218-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y))-2.3800027794354056e-8*TMath::Power(TMath::Cos(TMath::Pi()/180*y),3)*TMath::Sqrt(2.1218-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y))+TMath::Power(x,2)*TMath::Power(TMath::Cos(TMath::Pi()/180*y),3)*(3.2818816073967673e-7*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))-1.1684275435535303e-6*TMath::Sqrt(2.1218-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y)))+x*TMath::Power(TMath::Cos(TMath::Pi()/180*y),3)*(-8.112811333484808e-8*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))+2.888352887664327e-7*TMath::Sqrt(2.1218-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y)))+TMath::Power(x,3)*TMath::Power(TMath::Cos(TMath::Pi()/180*y),3)*(-4.425406698215705e-7*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))+1.5755495463235305e-6*TMath::Sqrt(2.1218-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y)))+TMath::Power(TMath::Cos(TMath::Pi()/180*y),2)*(-6.315346819441329e-6*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))+0.00005334447875055668*TMath::Sqrt(2.1218-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y))+x*(0.00005109503899224376*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))-0.0004315896339041803*TMath::Sqrt(2.1218-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y)))+TMath::Power(x,2)*(-0.0001033475707771921*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))+0.0008729563792560281*TMath::Sqrt(2.1218-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y))))+TMath::Cos(TMath::Pi()/180*y)*(0.0014548779564248476*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))-0.014359425845202903*TMath::Sqrt(2.1218-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y))+x*(-0.005885428626314109*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))+0.05808829225405703*TMath::Sqrt(2.1218-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y))))))/((1-0.00040406601131876197*TMath::Cos(TMath::Pi()/180*y)+0.0016345712431988753*x*TMath::Cos(TMath::Pi()/180*y))*(1-0.0029397862016351797*TMath::Cos(TMath::Pi()/180*y)+0.011892339003378558*x*TMath::Cos(TMath::Pi()/180*y))*(1-0.005035070902595827*TMath::Cos(TMath::Pi()/180*y)+0.02036840980014493*x*TMath::Cos(TMath::Pi()/180*y))*(1-0.008226881320143641*TMath::Cos(TMath::Pi()/180*y)+0.03328026424006327*x*TMath::Cos(TMath::Pi()/180*y))*TMath::Power(2.1218-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y),2.67)*(-0.42008790004955787*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))+TMath::Sqrt(2.1218-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y))))"
ADarplus = "(0.04454993403165476*TMath::Exp(2.172701227027019/(0.1236*TMath::Cos(TMath::Pi()/180*y)-x*TMath::Cos(TMath::Pi()/180*y)-1.0609))*TMath::Power(TMath::Cos(TMath::Pi()/180*y),2.67-1.0106422229299041/(0.1236*TMath::Cos(TMath::Pi()/180*y)-x*TMath::Cos(TMath::Pi()/180*y)-1.0609))*(3.831797941255795e-9*TMath::Power(TMath::Cos(TMath::Pi()/180*y),3.5)-2.5067089548238198e-8*TMath::Power(TMath::Cos(TMath::Pi()/180*y),3)*TMath::Sqrt(-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y)+2.1218)+TMath::Power(x,2)*TMath::Power(TMath::Cos(TMath::Pi()/180*y),3)*(1.8811651375285701e-7*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))-1.230632086565563e-6*TMath::Sqrt(-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y)+2.1218))+x*TMath::Power(TMath::Cos(TMath::Pi()/180*y),3)*(-4.6502402199706266e-8*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))+3.042122517990072e-7*TMath::Sqrt(-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y)+2.1218))+TMath::Power(x,3)*TMath::Power(TMath::Cos(TMath::Pi()/180*y),3)*(-2.5366304443481265e-7*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))+1.6594283799427765e-6*TMath::Sqrt(-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y)+2.1218))+(0.09269410920144934*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))+TMath::Sqrt(-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y)+2.1218))+TMath::Power(TMath::Cos(TMath::Pi()/180*y),2)*(3.2762610110392485e-6*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))+0.00005369460580045414*TMath::Sqrt(-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y)+2.1218)+x*(-0.000026506966108731775*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))-0.0004344223770263279*TMath::Sqrt(-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y)+2.1218))+TMath::Power(x,2)*(0.00005361441365034748*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))+0.0008786860376746114*TMath::Sqrt(-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y)+2.1218)))+TMath::Cos(TMath::Pi()/180*y)*(-0.0012174109045183516*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))-0.014383269769682962*TMath::Sqrt(-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y)+2.1218)+x*(0.004924801393682649*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))+0.05818474825923528*TMath::Sqrt(-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y)+2.1218)))))/((-0.00040406601131876197*TMath::Cos(TMath::Pi()/180*y)+0.0016345712431988753*x*TMath::Cos(TMath::Pi()/180*y)+1)*(-0.0029397862016351797*TMath::Cos(TMath::Pi()/180*y)+0.011892339003378558*x*TMath::Cos(TMath::Pi()/180*y)+1)*(-0.005035070902595827*TMath::Cos(TMath::Pi()/180*y)+0.02036840980014493*x*TMath::Cos(TMath::Pi()/180*y)+1)*(-0.008226881320143641*TMath::Cos(TMath::Pi()/180*y)+0.03328026424006327*x*TMath::Cos(TMath::Pi()/180*y)+1)*TMath::Power(-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y)+2.1218,2.67)*(-0.42008790004955787*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))+TMath::Sqrt(-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y)+2.1218)))"
ADarminus = "(0.031055887893745797*TMath::Exp(2.172701227027019/(0.1236*TMath::Cos(TMath::Pi()/180*y)-x*TMath::Cos(TMath::Pi()/180*y)-1.0609))*TMath::Power(TMath::Cos(TMath::Pi()/180*y),2.67-1.0106422229299041/(0.1236*TMath::Cos(TMath::Pi()/180*y)-x*TMath::Cos(TMath::Pi()/180*y)-1.0609))*(1.0777836695267741e-8*TMath::Power(TMath::Cos(TMath::Pi()/180*y),3.5)-2.1982416984362076e-8*TMath::Power(TMath::Cos(TMath::Pi()/180*y),3)*TMath::Sqrt(-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y)+2.1218)+TMath::Power(x,2)*TMath::Power(TMath::Cos(TMath::Pi()/180*y),3)*(5.29122123868283e-7*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))-1.0791946001214612e-6*TMath::Sqrt(-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y)+2.1218))+x*TMath::Power(TMath::Cos(TMath::Pi()/180*y),3)*(-1.3079898902023958e-7*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))+2.667769051500252e-7*TMath::Sqrt(-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y)+2.1218))+TMath::Power(x,3)*TMath::Power(TMath::Cos(TMath::Pi()/180*y),3)*(-7.134872220446103e-7*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))+1.455224649570471e-6*TMath::Sqrt(-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y)+2.1218))+(-0.3655580074957874*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))+TMath::Sqrt(-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y)+2.1218))+TMath::Power(TMath::Cos(TMath::Pi()/180*y),2)*(-0.0000200745894328675*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))+0.00005284221853410446*TMath::Sqrt(-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y)+2.1218)+x*(0.0001624157721105785*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))-0.000427526039919939*TMath::Sqrt(-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y)+2.1218))+TMath::Power(x,2)*(-0.0003285108659194549*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))+0.0008647371357603943*TMath::Sqrt(-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y)+2.1218)))+TMath::Cos(TMath::Pi()/180*y)*(0.005288298944929909*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))-0.014325221533728156*TMath::Sqrt(-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y)+2.1218)+x*(-0.021392795084667918*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))+0.057949925298253054*TMath::Sqrt(-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y)+2.1218)))))/((-0.00040406601131876197*TMath::Cos(TMath::Pi()/180*y)+0.0016345712431988753*x*TMath::Cos(TMath::Pi()/180*y)+1)*(-0.0029397862016351797*TMath::Cos(TMath::Pi()/180*y)+0.011892339003378558*x*TMath::Cos(TMath::Pi()/180*y)+1)*(-0.005035070902595827*TMath::Cos(TMath::Pi()/180*y)+0.02036840980014493*x*TMath::Cos(TMath::Pi()/180*y)+1)*(-0.008226881320143641*TMath::Cos(TMath::Pi()/180*y)+0.03328026424006327*x*TMath::Cos(TMath::Pi()/180*y)+1)*TMath::Power(-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y)+2.1218,2.67)*(-0.42008790004955787*TMath::Sqrt(TMath::Cos(TMath::Pi()/180*y))+TMath::Sqrt(-0.2472*TMath::Cos(TMath::Pi()/180*y)+x*TMath::Cos(TMath::Pi()/180*y)+2.1218)))"
# The spectrum is simulated in two parts, in the range E = 1(or emin) to 10 GeV and in the range E = 10 to 100(or emax) GeV. 
# This allows better resolution of the steep peak at low energy and low zenith angle. Most muons have E < 10 GeV
cmmc_spec = ROOT.TF2("cmmc_spec",ADar,emin,emax,thmin,thmax)
cmmc_spec_plus = ROOT.TF2("cmmc_spec_plus",ADarplus,emin,emax,thmin,thmax)
cmmc_spec_minus = ROOT.TF2("cmmc_spec_minus",ADarminus,emin,emax,thmin,thmax)
# ADar*sin(theta) for integrating over theta later on
cmmc_spec_sin = ROOT.TF2("cmmc_spec_sin",ADar+"*TMath::Sin(TMath::Pi()/180*y)",emin,emax,thmin,thmax)
cmmc_spec1_sin = ROOT.TF2("cmmc_spec1_sin",ADar+"*TMath::Sin(TMath::Pi()/180*y)",emin,10.0,thmin,thmax)
# full spectrum split along 10 GeV:
cmmc_spec1 = ROOT.TF2("cmmc_spec1",ADar,emin,10.0,thmin,thmax)
cmmc_spec2 = ROOT.TF2("cmmc_spec2",ADar,10.0,emax,thmin,thmax)
# set the resolution over each energy range and over theta to 250 points.
cmmc_spec.SetNpx(250)
cmmc_spec.SetNpy(250)
cmmc_spec_sin.SetNpx(250)
cmmc_spec_sin.SetNpy(250)
cmmc_spec1_sin.SetNpx(250)
cmmc_spec1_sin.SetNpy(250)
cmmc_spec1.SetNpx(250)
cmmc_spec1.SetNpy(250)
cmmc_spec2.SetNpx(250)
cmmc_spec2.SetNpy(250)
# Find the fraction of events in the low E spectrum, this requires doing integrals over theta, so I need to use ADar*Sin(theta), the sine factor comes from dOmega
full_int = cmmc_spec_sin.Integral(emin,emax,thmin,thmax)
low_frac = cmmc_spec1_sin.Integral(emin,10,thmin,thmax)/full_int
# choose the correct hcal dimensions based on the user geometry choice. dx, dy, and dz are the full width, height, and depth of the detector in mm.
dx = 3100.
dy = 3100.
if arg.geometry == "v3" or arg.geometry == "v4":
  dz = 3290.
elif arg.geometry == "v5":
  dz = 3250.
elif arg.geometry == "v6":
  dz = 3282.
elif arg.geometry == "v7":
  dz = 6284.
elif arg.geometry == "v8":
  dz = 6274.
elif arg.geometry == "v9":
  dz = 4690.
elif arg.geometry == "v10":
  dx = 3000.
  dy = 3000.
  dz = 4690.
else:
  print "cosmic_muon_lhe_generator.py: geometry version "+arg.geometry+" not available."
# calculate the expected average rate of muons intersecting the hcal. muon flux through the top: 0.00785918 muons/cm^2/s, side: 0.00306525 muons/cm^2/s
# the factor of 100 is to change the dx, dy, and dz from mm to cm. 
# this calculation give the rate of muons entering the ldmx hcal per second, muons/s
# v3: 2015.9485132 muons/s
# v4: 2015.9485132 muons/s
# v5: 1998.60131 muons/s
# v6: 2012.47907256 muons/s
# v7: 3314.38667272 muons/s
# v8: 3310.04987192 muons/s
# v9: 2623.1006252 muons/s
# v10: 2520.092976 muons/s
total_rate = (0.00785918*dx*dz+0.00306525*2*dy*(dx+dz))/100
print "cosmic_muon_lhe_generator.py: physical rate: "+str(total_rate)+" muons/s"
# initialize, generate random numbers
E = ROOT.Double()
thdeg = ROOT.Double()
print "cosmic_muon_lhe_generator.py: running..."
for n in range(arg.numFiles):
  filename = "cosmic_muons_"+str(int(emin))+"_"+str(int(emax))+"_GeV_"+str(int(thmin))+"_"+str(int(thmax))+"_deg_"+str(arg.numEvents)+"_events_%s_detector_%04d.lhe"%(arg.geometry,n)
  new_lhe = open("%s%s"%(output,filename),"w")
  for i in range(arg.numEvents):
    rand = random.random()
    if rand <= low_frac: # E <= 10 GeV
      cmmc_spec1.GetRandom2(E,thdeg)
    else: # E > 10 GeV
      cmmc_spec2.GetRandom2(E,thdeg)
    # determine the charge of the muon
    flux_plus = cmmc_spec_plus.Eval(E,thdeg)
    flux_minus = cmmc_spec_minus.Eval(E,thdeg)
    flux_total = flux_plus + flux_minus
    prob_plus = flux_plus/flux_total
    rand_pm = random.random()
    if rand_pm < prob_plus:
      pdgID = -13
    else:
      pdgID = 13
    p = math.sqrt(math.pow(E,2)-math.pow(m,2))
    theta = thdeg*math.pi/180
    phi = random.uniform(0,360)
    # get the muon momentum in detector cooridinates (y-axis up and z-axis down-beam)
    px = -p*math.sin(theta)*math.sin(phi)
    py = -p*math.cos(theta)
    pz = -p*math.sin(theta)*math.cos(phi)
    # pick a random point inside the full hcal volume in detector coordinates, (0,0,0) is the center of the target
    xmin = -dx/2.
    xmax = dx/2.
    x = random.uniform(xmin,xmax)
    ymin = -dy/2.
    ymax = dy/2.
    y = random.uniform(ymin,ymax)
    zmin = 200.
    zmax = zmin + dz
    z = random.uniform(zmin,zmax)
    # find the intersection with the hcal volume
    # xt, yt, and zt are where the incoming muon would intersect infinite planes containing the planes of the hcal volume
    # check for muons intersecting the top plane first
    xt = x + px/py*(ymax-y)
    zt = z + pz/py*(ymax-y)
    if xmin < xt < xmax and zmin < zt < zmax:
      xv = xt
      yv = ymax
      zv = zt
    # now check for muons intersecting the positive x, negative x, positive z, and negative z planes
    else:
      if px < 0:
        yt = y + py/px*(xmax-x)
        zt = z + pz/px*(xmax-x)
        if ymin < yt < ymax and zmin < zt < zmax:
          xv = xmax
          yv = yt
          zv = zt
      elif px > 0:
        yt = y + py/px*(xmin-x)
        zt = z + pz/px*(xmin-x)
        if ymin < yt < ymax and zmin < zt < zmax:
          xv = xmin
          yv = yt
          zv = zt
      if pz < 0:
        xt = x + px/pz*(zmax-z)
        yt = y + py/pz*(zmax-z)
        if xmin < xt < xmax and ymin < yt < ymax:
          xv = xt
          yv = yt
          zv = zmax
      elif pz > 0:
        xt = x + px/pz*(zmin-z)
        yt = y + py/pz*(zmin-z)
        if xmin < xt < xmax and ymin < yt < ymax:
          xv = xt
          yv = yt
          zv = zmin
    new_lhe.write("<event>\n")
    new_lhe.write(" 1   0  0.3584989E-03  0.9118800E+02  0.7818608E-02  0.1180000E+00\n")
    new_lhe.write("#vertex %f %f %f\n"%(xv,yv,zv))
    new_lhe.write("%9d    1    0    0    0    0  %.11E  %.11E  %.11E  %.11E  %.11E 0. 1.\n"%(pdgID,px,py,pz,E,m))
    new_lhe.write("</event>\n")
  new_lhe.close()
print "cosmic_muon_lhe_generator.py: %d muons generated"%(arg.numEvents)
quit()
