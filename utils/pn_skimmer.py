
import argparse
import ROOT as r
import os

def main(): 

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-d', action='store', dest='dir', 
                        help='Directory containing the list of files to crawl.')
    parser.add_argument('-o', action='store', dest='output', 
                        help='Output directory.')
    parser.add_argument('-l', action='store', dest='lib') 
    args = parser.parse_args()

    if not args.dir:
        parser.error('Please specify a path to the files to be processed.')
    
    r.gSystem.Load(args.lib.strip())
    
    # Get the list of all files and directories and filter out the directory
    # names. 
    files = (file for file in os.listdir(args.dir.strip()) 
                     if os.path.isfile(os.path.join(args.dir.strip(), file)))
    
    for file_name in files: 


        f1 = r.TFile('%s/%s' % (args.dir.strip(), file_name.strip()))
        t1 = f1.Get('LDMX_Events')

        particles = r.TClonesArray('ldmx::SimParticle') 
        t1.SetBranchAddress('SimParticles_sim', particles)

        f3 = r.TFile('%s/%s' % (args.output.strip(), file_name.strip()), "recreate")
        t1_new = t1.CloneTree(0)

        for i in xrange(0, t1.GetEntries()): 
            t1.GetEntry(i)

            recoil_e = None
            for particle in particles: 
                if (particle.getPdgID() == 11) & (particle.getParentCount() == 0): 
                    recoil_e = particle
                    break

            if not recoil_e: continue

            # Search for the PN gamma and use it to get the PN daughters
            pn_gamma = None
            for daughter_count in xrange(0, recoil_e.getDaughterCount()):
                daughter = recoil_e.getDaughter(daughter_count)

                if (daughter.getDaughterCount() > 0) and \
                        (daughter.getDaughter(0).getProcessType() == 9): 
                    pn_gamma = daughter
                    break
    
            if not pn_gamma: continue 
        
            t1_new.Fill()

        t1_new.AutoSave()

        f1.Close()
        f3.Close()

if __name__ == "__main__":
    main()

