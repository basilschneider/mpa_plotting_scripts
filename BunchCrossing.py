#!/usr/bin/env python2

""" Author: Basil Schneider <basil.schneider@cern.ch>
Simple plotting script to visualize the output of the MPA Light synchronous
readout (bunch crossing data). """

from ROOT import gROOT, gStyle
from MPA import MPA

class BunchCrossing(object):

    """ Simple plotting class to visualize the output of the MPA Light
    synchronous readout (bunch crossing data). """

    # Global settings
    _no_mpas = 6
    _no_pxs_x = 16
    _no_pxs_y = 3
    _no_mems = 96

    # ROOT batch mode
    gROOT.SetBatch(True)
    # No statistics in plots
    gStyle.SetOptStat(0)

    def __init__(self):

        """ Initialize instances of class. """

        # Create 6 MPA objects
        self._MPAs = []
        for i in range(0, self._no_mpas):
            self._MPAs.append(MPA(self._no_mems))

    def read_data_raw(self, logfile):

        """ Read in raw logfile and fill MPA objects. """

        # Open raw logfile
        with open(logfile, 'r') as logfile:
            for idx, line in enumerate(logfile):
                # Each line corresponds to one MPA object
                # The correct MPA object is found by idx % len(MPA)
                self._MPAs[idx % len(self._MPAs)].\
                    set_no_hits_shutter([int(val) for val in line.split()])
