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

r.gROOT.ProcessLine('.L Loader.C+')

######################################################################
class sampleContainer:

	def __init__(self, fn, ofn):

		print "Hello In!"
		self.fin = r.TFile(fn);
		self.tin = self.fin.Get("LDMX_Events")
		self.nHCalLayers = 50;

		self.fn_out = ofn;
		self.fout = r.TFile(self.fn_out,"RECREATE");

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
		self.tin.SetBranchAddress("Trigger_recon",  r.AddressOf( self.trigRes ));
		self.tin.SetBranchAddress("SimParticles_sim",  r.AddressOf( self.simParticles ));
		self.tin.SetBranchAddress("EcalSimHits_sim",  r.AddressOf( self.ecalSimHits ));
		self.tin.SetBranchAddress("HcalSimHits_sim",  r.AddressOf( self.hcalSimHits ));
		self.tin.SetBranchAddress("hcalDigis_recon",  r.AddressOf( self.hcalHits ));
		self.tin.SetBranchAddress("ecalDigis_recon",  r.AddressOf( self.ecalHits ));
		self.tin.SetBranchAddress("EcalVeto_recon",  r.AddressOf( self.ecalVetoRes ));
		self.tin.SetBranchAddress("FindableTracks_recon",  r.AddressOf( self.trackRes ));

		#self.tin.SetBranchStatus("*sim*",0);

		# results
		self.tout = r.TTree("otree","otree");
		self.b_bTrig = array('f',[0.]);
		self.b_bMuons = array('f',[0.]);
		self.b_bHcalNoVeto = array('f',[0.]);
		self.b_bEcalNoVeto = array('f',[0.]);
		self.b_bTkNoVeto = array('f',[0.]);
		
		self.b_nTrack = array('f',[0.]);
		self.b_nTrack_4s = array('f',[0.]);
		self.b_nTrack_3s1a = array('f',[0.]);
		self.b_nMuons = array('f',[0.]);
		
		self.b_vMuonE = r.std.vector('float')();
		self.b_vMuonTh = r.std.vector('float')();

		self.tout.Branch("bTrig",self.b_bTrig,"bTrig/F");
		self.tout.Branch("bMuons",self.b_bMuons,"bMuons/F");
		self.tout.Branch("bHcalNoVeto",self.b_bHcalNoVeto,"bHcalNoVeto/F");
		self.tout.Branch("bEcalNoVeto",self.b_bEcalNoVeto,"bEcalNoVeto/F");
		self.tout.Branch("bTkNoVeto",self.b_bTkNoVeto,"bTkNoVeto/F");

		self.tout.Branch("nTrack",self.b_nTrack,"nTrack/F");
		self.tout.Branch("nTrack_4s",self.b_nTrack_4s,"nTrack_4s/F");
		self.tout.Branch("nTrack_3s1a",self.b_nTrack_3s1a,"nTrack_3s1a/F");
		self.tout.Branch("nMuons",self.b_nMuons,"nMuons/F");
		self.tout.Branch("muonE",self.b_vMuonE);
		self.tout.Branch("muonTh",self.b_vMuonTh);

		# # counting histograms
		# self.h_nTote = r.TH1F("h_nTote","h_nTote",1,0,1);
		# self.h_nTrig = r.TH1F("h_nTrig","h_nTrig",1,0,1);
		# self.h_nMuons = r.TH1F("h_nMuons","h_nMuons",10,0,10);
		# self.h_nHasMuons = r.TH1F("h_nHasMuons","h_nHasMuons",1,0,1);
		# self.h_nHCalVeto = r.TH1F("h_nHCalVeto","h_nHCalVeto",1,0,1);
		# self.h_nPassesEcalVeto = r.TH1F("h_nPassesEcalVeto","h_nPassesEcalVeto",1,0,1);
		# self.h_nTracks_4s = r.TH1F("h_nTracks_4s","h_nTracks_4s",9,0,9);
		# self.h_nTracks_3s1a = r.TH1F("h_nTracks_3s1a","h_nTracks_3s1a",9,0,9);
		# self.h_nTracks = r.TH1F("h_nTracks","h_nTracks",9,0,9);

		# # combo counters
		# self.h_nTrig_noHcalVeto = r.TH1F("h_nTrig_noHcalVeto","h_nTrig_noHcalVeto",1,0,1);
		# self.h_nPassesEcalVeto_nTrig_noHcalVeto = r.TH1F("h_nPassesEcalVeto_nTrig_noHcalVeto","h_nPassesEcalVeto_nTrig_noHcalVeto",1,0,1);

		# self.h_nTrig_noHcalVeto_hasMuons = r.TH1F("h_nTrig_noHcalVeto_hasMuons","h_nTrig_noHcalVeto_hasMuons",1,0,1);

		# self.h_muonEnergy = r.TH1F("h_muonEnergy","; E_{muon}; frac of events", 100, 0, 4000);
		# self.h_muonAngle = r.TH1F("h_muonAngle","; #Theta; frac of events", 100, 0, 180);

		self.hs_evDisp_Trig_NoHCalVeto_HasMuons = [];

		self.loop();
		self.writeOutHistos();

	def writeOutHistos(self):

		# self.h_nTote.Write();
		# self.h_nTrig.Write();
		# self.h_nMuons.Write();
		# self.h_nHasMuons.Write();
		# self.h_nHCalVeto.Write();
		# self.h_nPassesEcalVeto.Write();
		# self.h_nTracks.Write();
		# self.h_nTracks_4s.Write();
		# self.h_nTracks_3s1a.Write();

		# self.h_nTrig_noHcalVeto.Write();
		# self.h_nTrig_noHcalVeto_hasMuons.Write();

		for h in self.hs_evDisp_Trig_NoHCalVeto_HasMuons: h.Write();

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
			# clear vectors
			self.b_vMuonE.clear();
			self.b_vMuonTh.clear();

			# trigger info
			if self.trigRes[0].passed(): self.b_bTrig[0] = 1.;
			else: self.b_bTrig[0] = 0.;

			# ecal veto info
			if self.ecalVetoRes[0].passesVeto(): self.b_bEcalNoVeto[0] = 1.;
			else: self.b_bEcalNoVeto[0] = 0.;

			# track info
			ntracks = 0.;
			ntracks_4s = 0.;
			ntracks_3s1a = 0.;
			for i,t in enumerate(self.trackRes):
				if t.is4sFindable(): ntracks_4s += 1;
				if t.is3s1aFindable(): ntracks_3s1a += 1;
				if t.is4sFindable() or t.is3s1aFindable(): ntracks += 1;
			self.b_nTrack[0] = ntracks;
			self.b_nTrack_4s[0] = ntracks_4s;
			self.b_nTrack_3s1a[0] = ntracks_3s1a;
			if ntracks <= 1: self.b_bTkNoVeto[0] = 1.;
			else: self.b_bTkNoVeto[0] = 0.;

			# hcal veto info
			b_hcalvetoed = False;
			for ih,hit in enumerate(self.hcalHits):
				#print hit.getPE(), hit.getLayer();
				if hit.getPE() >= 8: 
					b_hcalvetoed = True;
					break;				
			if b_hcalvetoed: self.b_bHcalNoVeto[0] = 0.;
			else: self.b_bHcalNoVeto[0] = 1.;

			nmuons = 0.;
			for ip,par in enumerate(self.simParticles):
				if math.fabs(par.getPdgID()) == 13: 
					nmuons += 1;
					self.b_vMuonE.push_back( par.getEnergy() );
					px = par.getMomentum()[0]
					py = par.getMomentum()[1]
					pz = par.getMomentum()[2]
					theta = math.atan(math.sqrt(px*px + py*py)/pz) * 180/3.1415
					self.b_vMuonTh.push_back( theta );

			self.b_nMuons[0] = nmuons;
			if nmuons > 0: self.b_bMuons[0] = 1.;
			else: self.b_bMuons[0] = 0.;
				
			# if b_triggered and not b_hcalvetoed and nmuons > 0: 
			# 	self.h_nTrig_noHcalVeto_hasMuons.Fill(0.5);
			# 	# print "======= OMG OMG OMG ", i
			# 	for ip,par in enumerate(self.simParticles):
			# 		print "++", par.getPdgID(), par.getEnergy(), par.getMomentum()[0], par.getMomentum()[1], par.getMomentum()[2]
			# 		# if (par.getEnergy() > maxElEnergy) and (par.getPdgID() == 11):
			# 		# maxElEnergy = par.getEnergy(); 
			# 	# print self.ecalSimHits.GetEntries(), self.hcalSimHits.GetEntries(), self.ecalHits.GetEntries(), self.hcalHits.GetEntries()
				
			# 	tmph = r.TH3F("h_evdisp_"+str(i),";z;x;y",50,200,500,50,-300,300,50,-300,300);
			# 	for iesh,esh in enumerate(self.ecalSimHits):
			# 		# print iesh, esh.getPosition()[0], esh.getPosition()[1], esh.getPosition()[2], esh.getEdep()
			# 		tmph.Fill(esh.getPosition()[2], esh.getPosition()[0], esh.getPosition()[1], esh.getEdep())
			# 	for ihsh,hsh in enumerate(self.hcalSimHits):
			# 		# print ihsh, hsh.getPosition()[0], hsh.getPosition()[1], hsh.getPosition()[2], hsh.getEdep()
			# 		tmph.Fill(hsh.getPosition()[2], hsh.getPosition()[0], hsh.getPosition()[1], hsh.getEdep())
			# 	self.hs_evDisp_Trig_NoHCalVeto_HasMuons.append( tmph );
			# 	backsum = 0;
			# 	frontsum = 0;
			# 	for ieh,eh in enumerate(self.ecalHits):
			# 		print ieh, eh.getEnergy(), eh.getLayer()
			# 		if eh.getLayer() >= 20: backsum += eh.getEnergy();
			# 		else: frontsum += eh.getEnergy();
			# 	# print "Ecal energy..."
			# 	# print "backsum = ", backsum, ", frontsum = ", frontsum, ", triggerEsum = ", self.trigRes[0].getAlgoVar0();
			# 	# for ihh,hh in enumerate(self.hcalHits):
			# 		# print ihh, hh.getEnergy(), hh.getLayer()
			# # for ibin in range(firstMIPLayer): self.h_eff.SetBinContent( ibin+1, self.h_eff.GetBinContent(ibin+1) + 1 );

			self.tout.Fill();

		print "\n";

		# print "n total     = ", self.h_nTote.Integral();		
		# print "n triggered = ", self.h_nTrig.Integral();
		# print "n hcal veto = ", self.h_nHCalVeto.Integral();
		# print "n triggered, no hcal veto = ", self.h_nTrig_noHcalVeto.Integral();
		# print "n triggered, no hcal veto, has muons = ", self.h_nTrig_noHcalVeto_hasMuons.Integral();


######################################################################

def main(options,args) : 
	
	print "Hello!"
	sc = sampleContainer(options.ifile,options.ofile) ;

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
