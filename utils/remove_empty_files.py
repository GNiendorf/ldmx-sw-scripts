#!/usr/bin/env python

import os
import argparse

def main(): 

    # Parse command line arguments.  The only requirement is a path to the 
    # directory containing the files that will be checked.
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("-p", action='store', dest='path',
                        help="Path to location where files are stored.")
    args = parser.parse_args()

    # If the path isn't specified, exit the application.
    if not args.path: 
        parser.error('A path to the files to rename needs to be provided.')

    # Loop through all of the files in a directory and check if they are
    # empty.  If so, remove them.
    for file_name in os.listdir(args.path):
        
        if os.stat('%s%s' % (args.path, file_name)).st_size == 0:
            print 'File %s%s is empty ... removing it.' % (args.path, file_name) 
            os.remove('%s%s' % (args.path, file_name)) 

if __name__ == "__main__" : 
    main()
