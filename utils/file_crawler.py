#!/usr/bin/python

import argparse
import sys
import ROOT as r
import os

def main() : 
   
    # Parse all command line arguments using the argparse module
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-d', action='store', dest='dir', 
                        help='Directory containing the list of files to crawl.')
    parser.add_argument('-t', action='store', dest='tree', 
                        help='Name of the ROOT tree to crawl.')
    args = parser.parse_args()

    if not args.dir:
        parser.error('Please specify a path to the files that will be processed.')
   
    total_entries = 0
    for file_name in os.listdir(args.dir): 
        print 'Crawling file %s' % file_name.strip()
        root_file = r.TFile('%s/%s' % (args.dir, file_name.strip()))
        tree = root_file.Get(args.tree.strip())
        if tree is None: 
            print 'File is empty.'
            continue
        total_entries += tree.GetEntries()
        root_file.Close()

    print "Total number of entries %s" % total_entries

if __name__ == "__main__":
    main()
