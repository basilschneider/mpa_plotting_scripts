#!/usr/bin/env python2

""" Author: Basil Schneider <basil.schneider@cern.ch>
Simple plotting script to visualize the output of the MPA Light synchronous
readout (bunch crossing data). """

from os import system
from ROOT import TH1F, THStack, TLegend
from Plotter import Plotter

class BunchCrossing(Plotter):

    """ Simple plotting class to visualize the output of the MPA Light
    synchronous readout (bunch crossing data). """

    def __init__(self):

        """ Initialize class instances. """

        self._initialize_mpas(self._no_mems)

    def plot_cts_bx(self, path):

        """ Plots counts vs. bunch crossing. """

        system('mkdir -p %s' % path)
        name = 'counts_per_bx_MPA%s'
        x_title = 'BX'
        y_title = 'Event count'

        # Get number of shutters
        no_shutters = len(self._MPAs[0].get_no_hits_shutter())

        # Create THStack and its TLegend
        stack = THStack(name % ('all'), name % ('all'))
        leg = TLegend(.9, .5, 1., .9)

        # Get max of all MPA's
        max_bx = 0
        for MPA in self._MPAs:
            max_bx = max(max_bx, MPA.get_max())

        # Plots for each pixel and each MPA
        for idx_mpa, MPA in enumerate(self._MPAs):

            # Histogram for one MPA
            h_mpa = TH1F(name % (idx_mpa), name % (idx_mpa), 50, 0, max_bx)

            for shutter in range(0, no_shutters):
                for mem in range(0, self._no_mems):
                    if MPA.get_no_hits_shutter()[shutter][mem] != 0:
                        h_mpa.Fill(MPA.get_no_hits_shutter()[shutter][mem])

            self._save_histo(h_mpa, '%s/%s.pdf' % (path, name % (idx_mpa)),
                             x_title, y_title, logy=True)

            h_mpa.SetLineColor(self._get_fill_color(idx_mpa))
            stack.Add(h_mpa)
            leg.AddEntry(h_mpa, 'MPA%s' % idx_mpa, 'l')

        self._save_histo(stack, '%s/%s.pdf' % (path, name % ('all')),
                         x_title, y_title, leg, logy=True, draw_option='nostack')
