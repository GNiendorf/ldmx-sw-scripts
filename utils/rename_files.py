#!/usr/bin/env python

import os
import argparse

from termcolor import colored

def main(): 

    # Parse command line arguments.  The only requirement is a path to the 
    # directory containing the files we want to rename.
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("-p", action='store', dest='path',
                        help="Path to location where files are stored.")
    args = parser.parse_args()

    # If the path isn't specified, exit the application.
    if not args.path: 
        parser.error('A path to the files to rename needs to be provided.')

    # Remove the hex string and append a number to the file prefix which 
    # includes some zero padding. Then rename the existing file to the new 
    # file.
    counter = 0
    for file_name in os.listdir(args.path):

        # Strip the hex string from the file
        name = file_name[:file_name.rfind('_') + 1] 

        # Add a file number to the remaining file prefix
        name += str(counter).zfill(6) + ".root"

        # Rename the file
        print "Renaming %s ---> %s" % (colored('%s/%s' % (args.path, file_name), 'red'),
                colored('%s/%s' % (args.path, name), 'green'))
        os.rename('%s/%s' % (args.path, file_name), '%s/%s' % (args.path, name))

        counter += 1

if __name__ == "__main__" : 
    main()

