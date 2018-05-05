
import argparse
import ROOT as r


def main(): 

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f1', action='store', dest='f1', 
                        help='Path to the file that will be skimmed.')
    parser.add_argument('-o', action='store', dest='output', 
                        help='Output file name.')
    parser.add_argument('-l', action='store', dest='lib') 
    args = parser.parse_args()

    r.gSystem.Load(args.lib.strip())

    f1 = r.TFile(args.f1.strip())
    t1 = f1.Get('LDMX_Events')

    t2 = f1.Get('LDMX_Events_resim') 
    hcal_digis = r.TClonesArray('ldmx::HcalHit') 
    t2.SetBranchAddress('hcalDigis_recon', hcal_digis)

    f3 = r.TFile(args.output.strip(), "recreate")
    t1_new = t1.CloneTree(0)
    t2_new = t2.CloneTree(0)

    for i in xrange(0, t1.GetEntries()): 
        t1.GetEntry(i)
        t2.GetEntry(i)

        max_pe = 0
        for hit in hcal_digis: 
            max_pe = max(max_pe, hit.getPE())

        if max_pe < 8: 
            t1_new.Fill()
            t2_new.Fill()

    t1_new.AutoSave()
    t2_new.AutoSave()

    f1.Close()
    f3.Close()

if __name__ == "__main__":
    main()


