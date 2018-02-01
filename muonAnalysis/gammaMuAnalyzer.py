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
		# self.nHCalLayers = 50;
		self.tag = int(tag);

		self.fn_out = ofn;
		self.fout = r.TFile("hist_"+self.fn_out,"RECREATE");

		self.fn_sklim = ofn;
		self.fsklim = r.TFile("sklim_"+self.fn_sklim,"RECREATE");
		self.tsklim = self.tin.CloneTree(0);

		self.evHeader = r.ldmx.EventHeader()
		self.trigRes = r.TClonesArray('ldmx::TriggerResult')
		self.simParticles = r.TClonesArray('ldmx::SimParticle')
		self.ecalHits = r.TClonesArray('ldmx::EcalHit')
		self.hcalHits = r.TClonesArray('ldmx::HcalHit')
		self.ecalSimHits = r.TClonesArray('ldmx::SimCalorimeterHit');
		self.hcalSimHits = r.TClonesArray('ldmx::SimCalorimeterHit');
		self.ecalVetoRes = r.TClonesArray('ldmx::EcalVetoResult');
		self.trackRes    = r.TClonesArray('ldmx::FindableTrackResult');
		self.tin.SetBranchAddress("EventHeader",  r.AddressOf( self.evHeader ));
		self.tin.SetBranchAddress("Trigger_reco",  r.AddressOf( self.trigRes ));
		self.tin.SetBranchAddress("SimParticles_sim",  r.AddressOf( self.simParticles ));
		self.tin.SetBranchAddress("EcalSimHits_sim",  r.AddressOf( self.ecalSimHits ));
		self.tin.SetBranchAddress("HcalSimHits_sim",  r.AddressOf( self.hcalSimHits ));
		self.tin.SetBranchAddress("hcalDigis_reco",  r.AddressOf( self.hcalHits ));
		self.tin.SetBranchAddress("ecalDigis_reco",  r.AddressOf( self.ecalHits ));
		self.tin.SetBranchAddress("EcalVeto_reco",  r.AddressOf( self.ecalVetoRes ));
		self.tin.SetBranchAddress("FindableTracks_reco",  r.AddressOf( self.trackRes ));

		self.ecalSPHits = r.TClonesArray('ldmx::SimTrackerHit');
		self.tin.SetBranchAddress("EcalScoringPlaneHits_sim",  r.AddressOf( self.ecalSPHits ));

		# histograms
		self.histograms = {};
		## counting histograms
		self.histograms["b_total"]    = r.TH1F("b_total","; event bit; N", 2, -0.5, 1.5);
		self.histograms["b_trig"]     = r.TH1F("b_trig","; trigger bit; N", 2, -0.5, 1.5);
		self.histograms["b_hcalVeto"] = r.TH1F("b_hcalVeto","; hcal veto; N", 2, -0.5, 1.5);
		self.histograms["b_ecalVeto"] = r.TH1F("b_ecalVeto","; ecal veto; N", 2, -0.5, 1.5);
		self.histograms["b_trckVeto"] = r.TH1F("b_trckVeto","; trck veto; N", 2, -0.5, 1.5);
		self.histograms["b_hcalOrtrackVeto"] = r.TH1F("b_hcalOrtrackVeto","; hcal or track veto; N", 2, -0.5, 1.5);

		## ecal sim info
		self.histograms["f_edeptot_ecal"] = r.TH1F("f_edeptot_ecal","; ECAL e dep; N", 50, 0, 150);
		self.histograms["f_zavgeweight_ecal"] = r.TH1F("f_zavgeweight_ecal","; z position (E-weighted); N", 50, 200, 500);
		self.histograms["f_edeptot_ecal__nohcalveto"] = r.TH1F("f_edeptot_ecal__nohcalveto","; ECAL e dep; N", 50, 0, 150);
		self.histograms["f_zavgeweight_ecal__nohcalveto"] = r.TH1F("f_zavgeweight_ecal__nohcalveto","; z position (E-weighted); N", 50, 200, 500);
		## hcal sim info
		self.histograms["f_minhcalsimhit_xy"] = r.TH2F("f_minhcalsimhit_xy",";x pos;y pos",100,-1600,1600,100,-1600,1600);
		self.histograms["f_minhcalsimhit_rz"] = r.TH2F("f_minhcalsimhit_rz",";r pos;z pos",100,0,4500,100,0,3500);
		# track "reconstruction"
		self.histograms["f_ntracks"] = r.TH1F("f_ntracks",";n tracks;N",11,-0.5,10.5);
		self.histograms["f_ntracks__nohcalveto"] = r.TH1F("f_ntracks__nohcalveto",";n tracks;N",11,-0.5,10.5);
		# ecal reconstruction
		self.histograms["f_bdtval"] = r.TH1F("f_bdtval",";BDT;N",50,0,1);
		self.histograms["f_bdtval__nohcalveto"] = r.TH1F("f_bdtval__nohcalveto",";BDT;N",50,0,1);
		# hcal reconstruction
		self.histograms["f_nhcalhits"] = r.TH1F("f_nhcalhits",";n hits;N",201,-0.5,200.5);
		self.histograms["f_hcalhitPEs"] = r.TH1F("f_hcalhitPEs",";PEs;N",101,-0.5,100.5);
		self.histograms["f_hcalMaxPEs"] = r.TH1F("f_hcalMaxPEs","; PEs (max);N",101,-0.5,100.5);

		self.histograms["f_hcalMaxPEs_ntracks"]  = r.TH2F("f_hcalMaxPEs_ntracks","; PEs (max);N tracks",101,-0.5,100.5,11,-0.5,10.5);
		self.histograms["f_nhcalhits_ntracks"] = r.TH2F("f_nhcalhits_ntracks",";n hits;N tracks",201,-0.5,200.5,11,-0.5,10.5);

		## gen information
		# inclusive
		# not vetoed by hcal

		self.loop();
		self.writeOutHistos();

	def writeOutHistos(self):

		self.fout.cd();
		for key in self.histograms: 
			print key
			self.histograms[key].Write();
		self.fout.Close();

		self.fsklim.cd();
		self.tsklim.Write();
		self.fsklim.Close();

	####################################################
	### looping 
	####################################################
	def loop(self):

		# self.b_itag[0] = self.tag;
		nent = self.tin.GetEntriesFast();
		print "nent = ", nent
		for i in range(nent):
			# print("---",i);
			if(nent/100 > 0 and i % (1 * nent/100) == 0):
				sys.stdout.write("\r[" + "="*int(20*i/nent) + " " + str(round(100.*i/nent,0)) + "% done")
				sys.stdout.flush()
	
			self.tin.GetEntry(i);
						
			# event weight
			ew = 1./self.evHeader.getWeight();
			# ew = 1.;
			self.histograms["b_total"].Fill(1.,ew);

			# trigger info
			if self.trigRes[0].passed(): self.histograms["b_trig"].Fill(1.,ew);
			else:                        self.histograms["b_trig"].Fill(0.,ew);

			# ----------------------------------------------------------------------
			# the rest of the information is saved only if the trigger is passed
			if not self.trigRes[0].passed(): continue;

			# ecal veto info
			if self.ecalVetoRes[0].passesVeto(): self.histograms["b_ecalVeto"].Fill(1.,ew);
			else:                                self.histograms["b_ecalVeto"].Fill(0.,ew);
			self.histograms["f_bdtval"].Fill( self.ecalVetoRes[0].getDisc() );


			# # ecal sim info
			necalsimhits = 0;
			totale_ecalsimhits = 0;
			eweightedz = 0;
			for ih,h in enumerate(self.ecalSimHits):
				# print h.getEdep();
				necalsimhits+=1;
				totale_ecalsimhits += h.getEdep();
				eweightedz += h.getEdep()*h.getPosition()[2];
			# print "number of ecal sim hits and total energy = ", necalsimhits, totale_ecalsimhits
			eweightedz /= totale_ecalsimhits;
			self.histograms["f_edeptot_ecal"].Fill(totale_ecalsimhits);
			self.histograms["f_zavgeweight_ecal"].Fill(eweightedz);
			# print "totale_ecalsimhits = ", totale_ecalsimhits
			# print "eweightedz = ", eweightedz

			# # track info
			ntracks = 0.;
			ntracks_4s = 0.;
			ntracks_3s1a = 0.;
			for it,t in enumerate(self.trackRes):
				if t.is4sFindable(): ntracks_4s += 1;
				if t.is3s1aFindable(): ntracks_3s1a += 1;
				if t.is4sFindable() or t.is3s1aFindable(): ntracks += 1;
			self.histograms["f_ntracks"].Fill(ntracks);
			if ntracks <= 1: self.histograms["b_trckVeto"].Fill(0.);
			else:            self.histograms["b_trckVeto"].Fill(1.);
			# print "ntracks = ",ntracks

			
			# hcal veto info
			b_hcalvetoed = 0;
			nhcalhits = 0;
			maxPEs = 0;
			for ih,hit in enumerate(self.hcalHits):
				nhcalhits+=1;
				if hit.getPE() >= 8: b_hcalvetoed = 1;				
				self.histograms["f_hcalhitPEs"].Fill(hit.getPE());
				if hit.getPE() > maxPEs: maxPEs = hit.getPE();
			self.histograms["b_hcalVeto"].Fill( b_hcalvetoed );
			self.histograms["f_nhcalhits"].Fill(nhcalhits);
			self.histograms["f_hcalMaxPEs"].Fill(maxPEs);

			self.histograms["f_hcalMaxPEs_ntracks"].Fill(maxPEs,ntracks);
			self.histograms["f_nhcalhits_ntracks"].Fill(nhcalhits,ntracks);

			if b_hcalvetoed == 0:
				self.histograms["f_edeptot_ecal__nohcalveto"].Fill(totale_ecalsimhits);
				self.histograms["f_zavgeweight_ecal__nohcalveto"].Fill(eweightedz);
				self.histograms["f_ntracks__nohcalveto"].Fill(ntracks);
				self.histograms["f_bdtval__nohcalveto"].Fill( self.ecalVetoRes[0].getDisc() );
				self.tsklim.Fill(); # sklimming!!

			if b_hcalvetoed == 1:
				# hcal simhit info
				minr = 1e8;
				minz = 1e8;
				minx = 1e8;
				miny = 1e8;
				for ih,h in enumerate(self.hcalSimHits):
					if h.getEdep() > 1.0:
						curx = h.getPosition()[0];
						cury = h.getPosition()[1];
						curz = h.getPosition()[2];
						curr = math.sqrt(curx*curx + cury*cury);
						if curr < minr: 
							minr = curr; minx = curx; miny = cury; minz = curz;
				self.histograms["f_minhcalsimhit_xy"].Fill( minx, miny );
				self.histograms["f_minhcalsimhit_rz"].Fill( minz, minr );

			if ntracks <= 1 and b_hcalvetoed == 0: self.histograms["b_hcalOrtrackVeto"].Fill(0.);
			else                                 : self.histograms["b_hcalOrtrackVeto"].Fill(1.);

			# print "xpos \t y pos \t z pos \t simpdgid \t simE \t id \t px \t py \t pz";
			# for ih,h in enumerate(self.ecalSPHits):
			# 	print "%0.1f \t %0.1f \t %0.1f \t %i \t %0.4f \t %i \t %0.2f \t %0.2f \t %0.2f" % (h.getPosition()[0], h.getPosition()[1], h.getPosition()[2], h.getSimParticle().getPdgID(), h.getSimParticle().getEnergy(), h.getID(), h.getMomentum()[0], h.getMomentum()[1], h.getMomentum()[2]);

			# if i > 200: break;
			
			# self.tout.Fill();

		print "\n";

######################################################################

def main(options,args) : 
	
	print "Hello!"
	sc = sampleContainer(options.ifile,options.ofile,options.tag) ;

def makeCanvas(hists, tags, norm=False, logy=True):

	colors = [1,2,4,6,7]

	leg = r.TLegend(0.6,0.7,0.85,0.9);
	leg.SetBorderSize(0);
	leg.SetFillStyle(0);
	leg.SetTextSize(0.04);
	leg.SetTextFont(42);
	tmax = -999;
	tmin = 9999;
	for i in range(len(hists)):
		leg.AddEntry(hists[i],tags[i],'l');
		if norm: hists[i].Scale(1./hists[i].Integral());
		if hists[i].GetMaximum() > tmax: tmax = hists[i].GetMaximum();
		if hists[i].GetMinimum() < tmin: tmin = hists[i].GetMinimum();

	c = r.TCanvas("c","c",1000,800);
	hists[0].SetMinimum(1e-7);
	hists[0].SetMaximum(tmax*1.2);
	for i in range(len(hists)):
		if i == 0: hists[i].Draw();
		else: 
			hists[i].SetLineColor( colors[i] );
			hists[i].Draw('sames');

	leg.Draw();
	r.gPad.SetLogy();
	c.SaveAs("plots/"+hists[0].GetName()+".pdf")
	c.SaveAs("plots/"+hists[0].GetName()+".png")


if __name__ == "__main__":
	
	parser = OptionParser()
	parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
	parser.add_option("--lumi", dest="lumi", type=float, default = 30,help="luminosity", metavar="lumi")
	parser.add_option('-i','--ifile', dest='ifile', default = 'file.root',help='directory with data', metavar='idir')
	parser.add_option('-o','--ofile', dest='ofile', default = 'ofile.root',help='directory to write plots', metavar='odir')
	parser.add_option('--swdir', dest='swdir', default = '/u/ey/ntran/ldmx/biasing/iss94/ldmx-sw',help='directory to write plots', metavar='odir')
	parser.add_option('--tag', dest='tag', default = '1',help='file tag', metavar='tag')

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
	r.gSystem.Load("/u/ey/ntran/ldmx/dev/reco/ldmx-sw/install/lib/libEvent.so");	

	main(options,args);
