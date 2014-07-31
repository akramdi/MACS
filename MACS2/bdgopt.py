# Time-stamp: <2014-07-30 23:06:58 Tao Liu>

"""Description: Modify bedGraph file

Copyright (c) 2014 Tao Liu <tliu4@buffalo.edu>

This code is free software; you can redistribute it and/or modify it
under the terms of the BSD License (see the file COPYING included with
the distribution).

@status:  experimental
@version: $Revision$
@author:  Tao Liu
@contact: tliu4@buffalo.edu
"""

# ------------------------------------
# python modules
# ------------------------------------
import sys
import os
import logging
from MACS2.IO import cBedGraphIO
from MACS2.OptValidator import opt_validate_bdgopt as opt_validate

# ------------------------------------
# constants
# ------------------------------------
logging.basicConfig(level=20,
                    format='%(levelname)-5s @ %(asctime)s: %(message)s ',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    stream=sys.stderr,
                    filemode="w"
                    )

# ------------------------------------
# Misc functions
# ------------------------------------
error   = logging.critical		# function alias
warn    = logging.warning
debug   = logging.debug
info    = logging.info
# ------------------------------------
# Classes
# ------------------------------------

# ------------------------------------
# Main function
# ------------------------------------
def run( options ):
    options = opt_validate( options )
    info("Read and build bedGraph...")
    bio = cBedGraphIO.bedGraphIO(options.ifile)
    btrack = bio.build_bdgtrack(baseline_value=0)

    info("Modify bedGraph...")
    if options.method.lower() == "multiply":
        btrack.apply_func( lambda x: x * options.extraparam)
    elif options.method.lower() == "add":
        btrack.apply_func( lambda x: x + options.extraparam)
    elif options.method.lower() == "p2q":
        btrack.p2q()
        
    ofile = os.path.join( options.outdir, options.ofile )
    info("Write bedGraph of modified scores...")
    ofhd = open(ofile,"wb")
    btrack.write_bedGraph(ofhd,name="%s_modified_scores" % (options.method.upper()),description="Scores calculated by %s" % (options.method.upper()))
    info("Finished '%s'! Please check '%s'!" % (options.method, ofile))



