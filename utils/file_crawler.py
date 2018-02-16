#!/usr/bin/python

import argparse
import sys
import ROOT as r
import os

from rootpy.io import root_open
from rootpy.io import DoesNotExist

def main() : 
   
    # Parse all command line arguments using the argparse module. All that
    # is currently required is the directory containing the files to crawl
    # and the name of the ROOT tree containing the data.
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-d', action='store', dest='dir', 
                        help='Directory containing the list of files to crawl.')
    parser.add_argument('-t', action='store', dest='tree', 
                        help='Name of the ROOT tree to crawl.')
    args = parser.parse_args()

    if not args.dir:
        parser.error('Please specify a path to the files to be processed.')
  
    # Get the list of all files and directories and filter out the directory
    # names. 
    files = (file for file in os.listdir(args.dir.strip()) 
                     if os.path.isfile(os.path.join(args.dir.strip(), file)))

    total_files = 0
    total_entries = 0
    for file_name in files: 
        print 'Crawling file %s' % file_name.strip()
        root_file = root_open('%s/%s' % (args.dir.strip(), file_name.strip()))
        try:
            tree = root_file.Get(args.tree.strip())
        except DoesNotExist:
            print 'Moving %s to trash.' % file_name.strip()
            if not os.path.exists('%s/trash' % args.dir.strip()):
                os.makedirs('%s/trash' % args.dir.strip())
            root_file.Close()
            os.rename('%s/%s' % (args.dir.strip(), file_name.strip()), 
                        '%s/trash/%s' % (args.dir.strip(), file_name.strip()))
            continue
        total_entries += tree.GetEntries()
        total_files += 1
        root_file.Close()

    print 'Finished crawling a total number of %s files containing %s entries' % (total_files, total_entries)

if __name__ == "__main__":
    main()
