#!/bin/python3.4
import sys, getopt
import time
import math
import datetime
import csv
import yaml

import bin2csv

def direct_report(nda_path, out_dir='.', config_file=None, log_file=None):
    """
    Takes an NDA path, digests the file and generates a complete report.
    Reports will be several files in a particular directory, for easy 
    compression and whatnot. 

    Config file should someday play a role, as well as a log file to track
    which files you haven't done yet.
    """
    # Config file nonsense
    report_format = 'txt'
    graphs = [('record_id', 'voltage'), ('record_id', 'current')]
    outname = None  # determine in program
    # End config

    csv_report = bin2csv.process_nda(nda_path, outpath=':mem:')
    ofile = open(out_dir + '/stuff.csv', 'w')
    ofile.write(csv_report.getvalue())
    #if not os.path.exists(directory):
            #os.makedirs(directory)
if __name__ == "__main__":
        direct_report(sys.argv[1])
