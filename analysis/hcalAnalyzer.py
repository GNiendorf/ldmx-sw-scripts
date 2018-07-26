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
		self.simParticles = r.TClonesArray('ldmx::SimParticle')
		self.hcalHits = r.TClonesArray('ldmx::HcalHit')
		self.hcalSimHits = r.TClonesArray('ldmx::SimCalorimeterHit');
		self.tin.SetBranchAddress("EventHeader",  r.AddressOf( self.evHeader ));
		self.tin.SetBranchAddress("hcalDigis_recon",  r.AddressOf( self.hcalHits ));

		# histograms
		self.histograms = {};

		self.histograms["hit_x"]= r.TH1F("hit_x","; hit x (mm); N", 400, -2000, 2000);
		self.histograms["hit_y"] = r.TH1F("hit_y","; hit y (mm); N", 400, -2000, 2000);
		self.histograms["hit_z"] = r.TH1F("hit_z","; hit z (mm); N", 400, 0, 4000);

		self.histograms["hit_strip"]   = r.TH1F("hit_strip","; hit strip; N", 100, 0, 100);		
		self.histograms["hit_layer"]   = r.TH1F("hit_layer","; hit_layer; N", 100, 0, 100);		
		self.histograms["hit_section"] = r.TH1F("hit_section","; hit_section; N", 10, 0, 10);		
	
		self.histograms["hit_PEs"] = r.TH1F("hit_PEs","; hit PEs; N", 80, 0, 4000);		    
		self.histograms["hit_MinPEs"] = r.TH1F("hit_MinPEs","; hit minPEs; N", 50, 0, 2000);		    
		self.histograms["event_MaxPE"] = r.TH1F("event_MaxPE","; event maxPEs; N", 50, 0, 5000);		    

		self.histograms["hit_PEs_back"] = r.TH1F("hit_PEs_back","; hit PEs; N", 10, 0, 10);		    
		self.histograms["hit_MinPEs_back"] = r.TH1F("hit_MinPEs_back","; hit minPEs; N", 10, 0, 10);		    
		self.histograms["event_MaxPE_back"] = r.TH1F("event_MaxPE_back","; event maxPEs; N", 10, 0, 10);		    
		self.histograms["hit_PEs_side"] = r.TH1F("hit_PEs_side","; hit PEs; N", 10, 0, 10);		    
		self.histograms["hit_MinPEs_side"] = r.TH1F("hit_MinPEs_side","; hit minPEs; N", 10, 0, 10);		    
		self.histograms["event_MaxPE_side"] = r.TH1F("event_MaxPE_side","; event maxPEs; N", 10, 0, 10);	

		self.histograms["hit_strip_v_z"]   = r.TH2F("hit_strip_v_z","; hit strip; hit z (mm)", 100, 0, 100, 400, 0, 4000);		
		self.histograms["hit_strip_v_layer"]   = r.TH2F("hit_strip_v_layer","; hit strip; hit layer", 100, 0, 100, 100, 0, 100);		
		
		self.histograms["hit_PEs_v_hit_MinPEs"]      = r.TH2F("hit_PEs_v_hit_MinPEs","; hit PEs; hit MinPEs", 10, 0, 10, 10, 0, 10);		    		
		self.histograms["hit_PEs_v_hit_MinPEs_back"] = r.TH2F("hit_PEs_v_hit_MinPEs_back","; hit PEs; hit MinPEs", 10, 0, 10, 10, 0, 10);		    
		self.histograms["hit_PEs_v_hit_MinPEs_side"] = r.TH2F("hit_PEs_v_hit_MinPEs_side","; hit PEs; hit MinPEs", 10, 0, 10, 10, 0, 10);		    


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
						
			# hcal veto info
			maxPEs = 0;
			maxPEs_back = 0;
			maxPEs_side = 0;
			for ih,hit in enumerate(self.hcalHits):				
				#print "hit PEs = ", hit.getPE(),", hit MinPEs = ",hit.getMinPE(),",\t id = ", hit.getID(), ", layer = ", hit.getLayer(), ", section = ", hit.getSection(), ", strip = ", hit.getStrip(), ", hit X = ", hit.getX(),", hit Y = ", hit.getY(),", hit Z = ", hit.getZ();
				self.histograms["hit_x"].Fill(hit.getX());
				self.histograms["hit_y"].Fill(hit.getY());
				self.histograms["hit_z"].Fill(hit.getZ());
				self.histograms["hit_strip"].Fill(hit.getStrip());
				self.histograms["hit_layer"].Fill(hit.getLayer());
				self.histograms["hit_section"].Fill(hit.getSection());
				self.histograms["hit_PEs"].Fill(hit.getPE());
				self.histograms["hit_MinPEs"].Fill(hit.getMinPE());

				self.histograms["hit_PEs_v_hit_MinPEs"].Fill(hit.getPE(),hit.getMinPE());
				if hit.getSection() == 0:
					self.histograms["hit_PEs_back"].Fill(hit.getPE());
					self.histograms["hit_MinPEs_back"].Fill(hit.getMinPE());
					self.histograms["hit_PEs_v_hit_MinPEs_back"].Fill(hit.getPE(),hit.getMinPE());
				else:					
					self.histograms["hit_PEs_side"].Fill(hit.getPE());
					self.histograms["hit_MinPEs_side"].Fill(hit.getMinPE());
					self.histograms["hit_PEs_v_hit_MinPEs_side"].Fill(hit.getPE(),hit.getMinPE());

				self.histograms["hit_strip_v_z"].Fill(hit.getStrip(),hit.getZ());
				self.histograms["hit_strip_v_layer"].Fill(hit.getStrip(),hit.getLayer());

				# if (hit.getStrip() > 31 and hit.getSection() == 0):
				# 	print "%i %i %i %0.4f %0.4f" % (hit.getStrip(),hit.getLayer(), hit.getPE(), hit.getX(), hit.getY())

				# if hit.getPE() >= 8: 
				# 	b_hcalvetoed = 1;				
				# 	nhcalhits+=1;
				# # self.histograms["f_hcalhitPEs"].Fill(hit.getPE());
				if hit.getMinPE() > 0 and hit.getPE() > maxPEs: maxPEs = hit.getPE();
				if hit.getMinPE() > 0 and hit.getPE() > maxPEs_back and hit.getSection() == 0: maxPEs_back = hit.getPE();
				if hit.getMinPE() > 0 and hit.getPE() > maxPEs_side and hit.getSection() > 0:  maxPEs_side = hit.getPE();
				# sumPEs += hit.getPE();
			self.histograms["event_MaxPE"].Fill(maxPEs);
			self.histograms["event_MaxPE_back"].Fill(maxPEs_back);
			self.histograms["event_MaxPE_side"].Fill(maxPEs_side);

			# self.histograms["b_hcalVeto"].Fill( b_hcalvetoed );
			# self.histograms["f_nhcalhits"].Fill(nhcalhits);
			# self.histograms["f_hcalMaxPEs"].Fill(maxPEs);
			# self.histograms["f_hcalSumPEs"].Fill(sumPEs);

			# if self.ecalVetoRes[0].getDisc() > 0.94:
			# 	self.histograms["f_nhcalhits__noecalveto"].Fill(nhcalhits);
			# 	self.histograms["f_hcalMaxPEs__noecalveto"].Fill(maxPEs);
			# 	if ntracks <= 1:  
			# 		self.histograms["f_nhcalhits__noecaltrkveto"].Fill(nhcalhits);
			# 		self.histograms["f_hcalMaxPEs__noecaltrkveto"].Fill(maxPEs);
											
			# # 2d information
			# self.histograms["f_hcalMaxPEs_ntracks"].Fill(maxPEs,ntracks);
			# self.histograms["f_nhcalhits_ntracks"].Fill(nhcalhits,ntracks);
			# self.histograms["f_hcalSumPEs_nhcalhits"].Fill(sumPEs,nhcalhits);
			# self.histograms["f_bdtVal_ntracks"].Fill(self.ecalVetoRes[0].getDisc(),ntracks);

			# if b_hcalvetoed == 0:
			# 	self.histograms["f_edeptot_ecal__nohcalveto"].Fill(totale_ecalsimhits);
			# 	self.histograms["f_zavgeweight_ecal__nohcalveto"].Fill(eweightedz);
			# 	self.histograms["f_ntracks__nohcalveto"].Fill(ntracks);
			# 	self.histograms["f_bdtval__nohcalveto"].Fill( self.ecalVetoRes[0].getDisc() );
			# 	self.tsklim.Fill(); # sklimming!!
			# 	if ntracks <= 1: 
			# 		self.histograms["f_bdtval__nohcaltrkveto"].Fill( self.ecalVetoRes[0].getDisc() );

			# if b_hcalvetoed == 1:
			# 	# hcal simhit info
			# 	minr = 1e8;
			# 	minz = 1e8;
			# 	minx = 1e8;
			# 	miny = 1e8;
			# 	for ih,h in enumerate(self.hcalSimHits):
			# 		if h.getEdep() > 1.0:
			# 			curx = h.getPosition()[0];
			# 			cury = h.getPosition()[1];
			# 			curz = h.getPosition()[2];
			# 			curr = math.sqrt(curx*curx + cury*cury);
			# 			if curr < minr: 
			# 				minr = curr; minx = curx; miny = cury; minz = curz;
			# 	self.histograms["f_minhcalsimhit_xy"].Fill( minx, miny );
			# 	self.histograms["f_minhcalsimhit_rz"].Fill( minz, minr );

			# if ntracks <= 1 and b_hcalvetoed == 0: self.histograms["b_hcalOrtrackVeto"].Fill(0.);
			# else                                 : self.histograms["b_hcalOrtrackVeto"].Fill(1.);

			# print "xpos \t y pos \t z pos \t simpdgid \t simE \t id \t px \t py \t pz";
			# for ih,h in enumerate(self.ecalSPHits):
			# 	print "%0.1f \t %0.1f \t %0.1f \t %i \t %0.4f \t %i \t %0.2f \t %0.2f \t %0.2f" % (h.getPosition()[0], h.getPosition()[1], h.getPosition()[2], h.getSimParticle().getPdgID(), h.getSimParticle().getEnergy(), h.getID(), h.getMomentum()[0], h.getMomentum()[1], h.getMomentum()[2]);

			if i > 1000: break;
			
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
	#parser.add_option("--lumi", dest="lumi", type=float, default = 30,help="luminosity", metavar="lumi")
	parser.add_option('-i','--ifile', dest='ifile', default = 'file.root',help='directory with data', metavar='idir')
	parser.add_option('-o','--ofile', dest='ofile', default = 'ofile.root',help='directory to write plots', metavar='odir')
	#parser.add_option('--swdir', dest='swdir', default = '/u/ey/ntran/ldmx/biasing/iss94/ldmx-sw',help='directory to write plots', metavar='odir')
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
	r.gSystem.Load("/u/ey/ntran/ldmx/dev/Jun2918/ldmx-sw-hcaldev/install/lib/libEvent.so");	

	main(options,args);
