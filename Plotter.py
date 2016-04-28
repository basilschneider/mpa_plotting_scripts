#!/usr/bin/env python2

""" Author: Basil Schneider <basil.schneider@cern.ch>
Parent class for plotting scripts to visualize the output of the MPA Light. """

from ROOT import gROOT, TCanvas, gStyle
from MPA import MPA

class Plotter(object):

    """ Simple plotting class to visualize the output of the MPA Light. """

    # Global settings
    _no_mpas = 6
    _no_pxs_x = 16
    _no_pxs_y = 3
    _no_mems = 96

    # ROOT batch mode
    gROOT.SetBatch(True)
    # No statistics in plots
    gStyle.SetOptStat(0)

    def _initialize_mpas(self, size):

        """ Initialize MPA objects. """

        # Create 6 MPA objects
        self._MPAs = []
        for i in range(0, self._no_mpas):
            self._MPAs.append(MPA(size))

    def get_mpas(self):

        """ Return list of MPA objects. """

        return self._MPAs

    def read_data_raw(self, logfile):

        """ Read in raw logfile and fill MPA objects. """

        # Open raw logfile
        with open(logfile, 'r') as logfile:
            for idx, line in enumerate(logfile):
                # Each line corresponds to one MPA object
                # The correct MPA object is found by idx % len(MPA)
                self._MPAs[idx % len(self._MPAs)].set_no_hits_shutter([int(val) for val
                                                           in line.split()])

    def _save_histo(self, histogram, path, x_title='', y_title='',
                    leg=None, draw_option='', logy=False, max=None, min=None):

        """ Plot and save histogram as PDF. """

        canvas = TCanvas()
        histogram.Draw(draw_option)
        histogram.GetXaxis().SetTitle(x_title)
        histogram.GetYaxis().SetTitle(y_title)
        if not min == None:
            histogram.SetMinimum(min)
        if not max == None:
            histogram.SetMaximum(max)
        if logy:
            canvas.SetLogy()
        if leg != None:
            leg.Draw()
        canvas.SaveAs(path)

    def _get_fill_color(self, idx):

        """ Return a fill color. """

        return idx+2

    def _get_mpa_coordinate(self, coordinate):

        """ Return physical coordinate of MPA on MaPSA assembly. """

        if coordinate == 0:
            return 1
        if coordinate == 1:
            return 2
        if coordinate == 2:
            return 3
        if coordinate == 3:
            return 6
        if coordinate == 4:
            return 5
        if coordinate == 5:
            return 4
        else:
            return -1
