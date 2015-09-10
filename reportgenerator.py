#!/bin/python3.4
import sys, getopt
import os
import time, datetime
import math
import datetime
import csv
import yaml

import matplotlib.pyplot as plt
import numpy as np
from io import StringIO

import bin2csv
import graph

def meta_process(m, level=4):
    # TODO: custom formats
    r = m['year'] + '-' + m['month'] + '-' + m['day']
    if level <= 1:
        return r

    r += ' ' + m['hour'] + ':' + m['minute'] + ':' + m['second']
    if level <= 2:
        return r
    
    r += ' on ' + str(m['machine']) + '_' + str(m['channel'])
    return r


def direct_report(nda_path, out_dir='.', config_file=None, log_file=None):
    """
    Takes an NDA path, digests the file and generates a complete report.
    Reports will be several files in a particular directory, for easy 
    compression and whatnot. 

    Config file should someday play a role, as well as a log file to track
    which files you haven't done yet.

    out_dir can end in a slash or not, linux doesn't seem to care about multi
    slash situations
    """
    # Config file nonsense
    report_format = 'txt'
    graphs = [('record_id', 'voltage', 'current'), 
            ('record_id', 'charge_mAh', 'energy_mWh')]
    outname = None  # determine in program
    overwrite = True
    # End config
    
    try:
        csv_report, m, lline = bin2csv.process_nda(nda_path, outpath=':mem:')
    except RuntimeError as e:
        # TODO: log e
        print(e)
        return False
    
    if outname is None:
        outname = out_dir + '/' + meta_process(m) 
    
    if not os.path.exists(outname):
        os.makedirs(outname)
    
    outcsv = outname + '/generalreport.csv'
    ofile = open(outcsv, 'w')
    ofile.write(csv_report.getvalue())
    ofile.close()
    
    for g in graphs:
        graph.multi_graph(outcsv, g[0], g[1:], outname)
    mdata = {}
    mdata['converted'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    mdata['started'] = meta_process(m, level=2)
    mdata['ended'] = lline[10]

    mdata['machine'] = m['machine']
    mdata['channel'] = m['channel']
    mdata['comments'] = m['comments']
    mdata['btsd version'] = m['version']
    mdata['user'] = m['name']
    
    mdata['file'] = nda_path

    mdata['modified'] = datetime.datetime.fromtimestamp(os.path.getmtime(nda_path))

    with open(outname + '/metadata.txt', 'w') as yfile:
        yfile.write(yaml.safe_dump(mdata, default_flow_style=False))
    print(outname)


if __name__ == "__main__":
    direct_report(sys.argv[1], out_dir='reports/')
