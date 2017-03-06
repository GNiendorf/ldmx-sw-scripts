#!/usr/bin/python
import argparse
import importlib
import ROOT as r
import os
import math
import sys
from array import array
from optparse import OptionParser
sys.path.insert(0, '../')

######################################################################
class sampleContainer:

	def __init__(self, fn, ofn, tag):

		self.fin = r.TFile(fn);
		self.tin = self.fin.Get("LDMX_Events")
		self.nHCalLayers = 50;
		self.tag = int(tag);

		self.evHeader = r.ldmx.EventHeader()
		self.simParticles = r.TClonesArray('ldmx::SimParticle')
		self.ecalSimHits = r.TClonesArray('ldmx::SimCalorimeterHit');
		self.hcalSimHits = r.TClonesArray('ldmx::SimCalorimeterHit');
		self.tin.SetBranchAddress("EventHeader",  r.AddressOf( self.evHeader ));
		self.tin.SetBranchAddress("SimParticles_sim",  r.AddressOf( self.simParticles ));
		self.tin.SetBranchAddress("EcalSimHits_sim",  r.AddressOf( self.ecalSimHits ));
		self.tin.SetBranchAddress("HcalSimHits_sim",  r.AddressOf( self.hcalSimHits ));

		self.fn_out = ofn;
		self.fout = r.TFile(self.fn_out,"RECREATE");
		self.tout = self.tin.CloneTree(0);

		for i in range(self.tin.GetEntries()):
			self.tin.GetEntry(i);
			if i > 50: self.tout.Fill();


		# results
		self.loop();
		self.writeOutHistos();

	def writeOutHistos(self):
		
		self.fout.cd();
		self.tout.Write();
		self.fout.Close();

	####################################################
	### looping 
	####################################################
	def loop(self):

		nent = self.tin.GetEntriesFast();
		print "nent = ", nent
		for i in range(nent):

			if(nent/100 > 0 and i % (1 * nent/100) == 0):
				sys.stdout.write("\r[" + "="*int(20*i/nent) + " " + str(round(100.*i/nent,0)) + "% done")
				sys.stdout.flush()
	
			self.tin.GetEntry(i);

			keepEvent = False;

			# ...
			if i > 50: keepEvent = True;

			if keepEvent: self.tout.Fill();

	# 	print "\n";

######################################################################

def main(options,args) : 
	
	print "Hello!"
	sc = sampleContainer(options.ifile,options.ofile,options.tag) ;

if __name__ == "__main__":
	
	parser = OptionParser()
	parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
	parser.add_option("--lumi", dest="lumi", type=float, default = 30,help="luminosity", metavar="lumi")
	parser.add_option('-i','--ifile', dest='ifile', default = 'file.root',help='directory with data', metavar='idir')
	parser.add_option('-o','--ofile', dest='ofile', default = 'ofile.root',help='directory to write plots', metavar='odir')
	parser.add_option('--swdir', dest='swdir', default = '/u/ey/ntran/ldmx/biasing/iss94/ldmx-sw',help='directory to write plots', metavar='odir')
	parser.add_option('--tag', dest='tag', default = '1',help='file tag', metavar='tag')
	parser.add_option('--pseudo', action='store_true', dest='pseudo', default =False,help='data = MC', metavar='isData')

	(options, args) = parser.parse_args()

	import tdrstyle
	tdrstyle.setTDRStyle()
	r.gStyle.SetPadTopMargin(0.10)
	r.gStyle.SetPadLeftMargin(0.16)
	r.gStyle.SetPadRightMargin(0.10)
	r.gStyle.SetPalette(1)
	r.gStyle.SetPaintTextFormat("1.1f")
	r.gStyle.SetOptFit(0000)
	r.gROOT.SetBatch()

	# Get the Event library 
	r.gSystem.Load(options.swdir+"/lib/libEvent.so");	

	main(options,args);
