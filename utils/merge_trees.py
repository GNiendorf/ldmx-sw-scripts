
import argparse
import ROOT as r


def main(): 

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f1', action='store', dest='f1', 
                        help='Path to first file.')
    parser.add_argument('-f2', action='store', dest='f2', 
                        help='Path to second file.')
    parser.add_argument('-o', action='store', dest='output', 
                        help='Output file name.')
    args = parser.parse_args()

    tree_name = 'LDMX_Events'
    f1 = r.TFile(args.f1.strip())
    t1 = f1.Get(tree_name)

    f2 = r.TFile(args.f2.strip())
    t2 = f2.Get(tree_name)

    f3 = r.TFile(args.output.strip(), "recreate")
    t1_new = t1.CloneTree(0)
    t2_new = t2.CloneTree(0)
    t2_new.SetName('LDMX_Events_resim')

    for i in xrange(0, t1.GetEntries()): 
        t1.GetEntry(i)
        t2.GetEntry(i)
        t1_new.Fill()
        t2_new.Fill()

    t1_new.AutoSave()
    t2_new.AutoSave()

    f1.Close()
    f2.Close()
    f3.Close()

if __name__ == "__main__":
    main()


