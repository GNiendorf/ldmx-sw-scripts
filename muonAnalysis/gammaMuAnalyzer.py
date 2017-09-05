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

	def __init__(self, fn, ofn, tag):

		print "Hello In!"
		self.fin = r.TFile(fn);
		self.tin = self.fin.Get("LDMX_Events")
		self.nHCalLayers = 50;
		self.tag = int(tag);

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
		self.b_itag = array('i',[0]);
		self.b_bTrig = array('f',[0.]);
		self.b_bMuons = array('f',[0.]);
		self.b_bHcalNoVeto = array('f',[0.]);
		self.b_bEcalNoVeto = array('f',[0.]);
		self.b_bTkNoVeto = array('f',[0.]);
		
		self.b_ecalV_LongestMipTrack = array('f',[0.]);
		self.b_ecalV_NMipTracks = array('f',[0.]);
		self.b_ecalV_SummedDet = array('f',[0.]);
		self.b_ecalV_SummedIso = array('f',[0.]);
		self.b_ecalV_SummedOuter = array('f',[0.]);

		self.b_nTrack = array('f',[0.]);
		self.b_nTrack_4s = array('f',[0.]);
		self.b_nTrack_3s1a = array('f',[0.]);
		self.b_nMuons = array('f',[0.]);
		
		self.b_vMuonE = r.std.vector('float')();
		self.b_vMuonTh = r.std.vector('float')();

		self.b_nHcalHits = array('f',[0.]);
		self.b_vHcalLayer = r.std.vector('float')();
		self.b_vHcalLayerPE = r.std.vector('float')();

		self.b_muonPhotonQ = array('f',[0.]);
		self.b_muonElectronQ = array('f',[0.]);
		self.b_photonElectronQ = array('f',[0.]);

		self.b_RminRhcalSimHit = array('f',[0.]);
		self.b_ZminRhcalSimHit = array('f',[0.]);
		self.b_EminRhcalSimHit = array('f',[0.]);

		self.tout.Branch("tag",self.b_itag,"tag/I");
		self.tout.Branch("bTrig",self.b_bTrig,"bTrig/F");
		self.tout.Branch("bMuons",self.b_bMuons,"bMuons/F");
		self.tout.Branch("bHcalNoVeto",self.b_bHcalNoVeto,"bHcalNoVeto/F");
		self.tout.Branch("bEcalNoVeto",self.b_bEcalNoVeto,"bEcalNoVeto/F");
		self.tout.Branch("bTkNoVeto",self.b_bTkNoVeto,"bTkNoVeto/F");

		self.tout.Branch("ecalV_LongestMipTrack",self.b_ecalV_LongestMipTrack,"ecalV_LongestMipTrack/F")
		self.tout.Branch("ecalV_NMipTracks",self.b_ecalV_NMipTracks,"ecalV_NMipTracks/F")
		self.tout.Branch("ecalV_SummedDet",self.b_ecalV_SummedDet,"ecalV_SummedDet/F")
		self.tout.Branch("ecalV_SummedIso",self.b_ecalV_SummedIso,"ecalV_SummedIso/F")
		self.tout.Branch("ecalV_SummedOuter",self.b_ecalV_SummedOuter,"ecalV_SummedOuter/F")

		self.tout.Branch("nTrack",self.b_nTrack,"nTrack/F");
		self.tout.Branch("nTrack_4s",self.b_nTrack_4s,"nTrack_4s/F");
		self.tout.Branch("nTrack_3s1a",self.b_nTrack_3s1a,"nTrack_3s1a/F");
		
		self.tout.Branch("nMuons",self.b_nMuons,"nMuons/F");
		self.tout.Branch("muonE",self.b_vMuonE);
		self.tout.Branch("muonTh",self.b_vMuonTh);

		self.tout.Branch("nHcalHits",self.b_nHcalHits,"nHcalHits/F");
		self.tout.Branch("hcalLayer",self.b_vHcalLayer);
		self.tout.Branch("hcalLayerPE",self.b_vHcalLayerPE);

		self.tout.Branch("muonPhotonQ",self.b_muonPhotonQ,"muonPhotonQ/F");
		self.tout.Branch("muonElectronQ",self.b_muonElectronQ,"muonElectronQ/F");
		self.tout.Branch("photonElectronQ",self.b_photonElectronQ,"photonElectronQ/F");

		self.tout.Branch("RminRhcalSimHit",self.b_RminRhcalSimHit,"RminRhcalSimHit/F");
		self.tout.Branch("ZminRhcalSimHit",self.b_ZminRhcalSimHit,"ZminRhcalSimHit/F");
		self.tout.Branch("EminRhcalSimHit",self.b_EminRhcalSimHit,"EminRhcalSimHit/F");

		self.hs_evDisp_Trig_NoHCalVeto_HasMuons = [];

		self.loop();
		self.writeOutHistos();

	def writeOutHistos(self):

		for h in self.hs_evDisp_Trig_NoHCalVeto_HasMuons: h.Write();

		self.tout.Write();
		self.fout.Close();

	####################################################
	### looping 
	####################################################
	def loop(self):

		self.b_itag[0] = self.tag;
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
			self.b_vHcalLayer.clear();
			self.b_vHcalLayerPE.clear();

			# trigger info
			if self.trigRes[0].passed(): self.b_bTrig[0] = 1.;
			else: self.b_bTrig[0] = 0.;

			# ecal veto info
			if self.ecalVetoRes[0].passesVeto(): self.b_bEcalNoVeto[0] = 1.;
			else: self.b_bEcalNoVeto[0] = 0.;
			self.b_ecalV_LongestMipTrack[0] = self.ecalVetoRes[0].getLongestMipTrack();
			self.b_ecalV_NMipTracks[0] = self.ecalVetoRes[0].getNMipTracks();
			self.b_ecalV_SummedDet[0] = self.ecalVetoRes[0].getSummedDet();
			self.b_ecalV_SummedIso[0] = self.ecalVetoRes[0].getSummedIso();
			self.b_ecalV_SummedOuter[0] = self.ecalVetoRes[0].getSummedOuter();

			# track info
			ntracks = 0.;
			ntracks_4s = 0.;
			ntracks_3s1a = 0.;
			for it,t in enumerate(self.trackRes):
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
			if b_hcalvetoed: 
				self.b_bHcalNoVeto[0] = 0.;
				self.b_nHcalHits[0] = 0.;
			else: 
				self.b_bHcalNoVeto[0] = 1.;
				self.b_nHcalHits[0] = float(self.hcalHits.GetEntries());
				for ih,hit in enumerate(self.hcalHits):
					self.b_vHcalLayer.push_back( hit.getLayer() );
					self.b_vHcalLayerPE.push_back( hit.getPE() );
			
			if not b_hcalvetoed and self.trigRes[0].passed():
				print "\n HCAL NOT VETOED Warning!", i
				nmuons=0
				for ip,par in enumerate(self.simParticles):
					if math.fabs(par.getPdgID()) == 13: 
						nmuons += 1;
						px = par.getMomentum()[0]
						py = par.getMomentum()[1]
						pz = par.getMomentum()[2]
						theta = math.atan2(math.sqrt(px*px + py*py),pz) * 180/3.1415
						print "NOT VETOED event -- muon ",nmuons,", e = ", par.getEnergy(), ", th = ", theta;	
				for ip,par in enumerate(self.simParticles):
					px = par.getMomentum()[0]
					py = par.getMomentum()[1]
					pz = par.getMomentum()[2]
					theta = math.atan2(math.sqrt(px*px + py*py),pz) * 180/3.1415
					print "NOT VETOED event -- particle ",par.getPdgID(),", e = %.2f, px,py,pz = %.2f,%.2f,%.2f" % (par.getEnergy(),px,py,pz);							
				print "\n";

			# muon info
			nmuons = 0.;
			for ip,par in enumerate(self.simParticles):
				if math.fabs(par.getPdgID()) == 13: 
					nmuons += 1;
					self.b_vMuonE.push_back( par.getEnergy() );
					px = par.getMomentum()[0]
					py = par.getMomentum()[1]
					pz = par.getMomentum()[2]
					theta = math.atan2(math.sqrt(px*px + py*py),pz) * 180/3.1415
					self.b_vMuonTh.push_back( theta );

			self.b_nMuons[0] = nmuons;
			if nmuons > 0: self.b_bMuons[0] = 1.;
			else: self.b_bMuons[0] = 0.;
				
			# Q^2 info
			rootElectron=None
			radiatedPhoton=None
			ConvMuonPlus=None
			ConvMuonMinus=None
			self.b_muonPhotonQ[0]=0.
			self.b_muonElectronQ[0]=0.
			self.b_photonElectronQ[0]=0.
			for p in self.simParticles :
				if p.getParentCount() != 0 : continue
				rootElectron = p
				for daughterIndex in range(p.getDaughterCount()) :
					daughter = p.getDaughter(daughterIndex)
					if daughter.getDaughterCount() == 2 and abs(daughter.getDaughter(0).getPdgID()) == 13 and abs(daughter.getDaughter(1).getPdgID()) == 13 :
						radiatedPhoton = daughter
						if( daughter.getDaughter(0).getPdgID() == 13 ):
							ConvMuonMinus = daughter.getDaughter(0)
							ConvMuonPlus = daughter.getDaughter(1)
						else : 
							ConvMuonMinus = daughter.getDaughter(1)
							ConvMuonPlus = daughter.getDaughter(0)

			if rootElectron!=None and radiatedPhoton!=None and ConvMuonPlus!=None and ConvMuonMinus!=None : 
				self.b_muonPhotonQ[0] = pow(pow(ConvMuonMinus.getMomentum()[0]+ConvMuonPlus.getMomentum()[0]-radiatedPhoton.getMomentum()[0],2)+pow(ConvMuonMinus.getMomentum()[1]+ConvMuonPlus.getMomentum()[1]-radiatedPhoton.getMomentum()[1],2)+pow(ConvMuonMinus.getMomentum()[2]+ConvMuonPlus.getMomentum()[2]-radiatedPhoton.getMomentum()[2],2),.5)

				self.b_muonElectronQ[0] = pow(pow(ConvMuonMinus.getMomentum()[0]+ConvMuonPlus.getMomentum()[0]-rootElectron.getMomentum()[0],2)+pow(ConvMuonMinus.getMomentum()[1]+ConvMuonPlus.getMomentum()[1]-rootElectron.getMomentum()[1],2)+pow(ConvMuonMinus.getMomentum()[2]+ConvMuonPlus.getMomentum()[2]-rootElectron.getMomentum()[2],2),.5)
				
				self.b_photonElectronQ[0] = pow(pow(radiatedPhoton.getMomentum()[0]-rootElectron.getMomentum()[0],2)+pow(radiatedPhoton.getMomentum()[2]-rootElectron.getMomentum()[2],2)+pow(radiatedPhoton.getMomentum()[2]-rootElectron.getMomentum()[2],2),0.5)

			# hcal sim hits
			self.b_RminRhcalSimHit[0] = 999999999.
			self.b_ZminRhcalSimHit[0] = 999999999.
			for hit in self.hcalSimHits : 
				if hit.getEdep()<1.0 : continue
				#print "hit position (x,y,z)",hit.getPosition()[0],hit.getPosition()[1],hit.getPosition()[2]
				r = pow(pow(hit.getPosition()[0],2)+pow(hit.getPosition()[1],2),0.5)
				#print "r",r
				if r < self.b_RminRhcalSimHit[0] :
					self.b_RminRhcalSimHit[0] = r
					self.b_ZminRhcalSimHit[0] = hit.getPosition()[2]
					self.b_EminRhcalSimHit[0] = hit.getEdep()

			self.tout.Fill();

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
