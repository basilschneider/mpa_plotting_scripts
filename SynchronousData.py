#!/usr/bin/env python2

""" Author: Basil Schneider <basil.schneider@cern.ch>
Simple plotting script to visualize the output of the MPA Light synchronous
readout (correlate hit maps with bunch crossing data). """

from os import system
from ROOT import TH1F, THStack, TLegend
from ROOT import kRed, kPink, kMagenta, kViolet, kBlue, kAzure
from ROOT import kCyan, kTeal, kGreen, kSpring, kYellow, kOrange
from Plotter import Plotter

class SynchronousData(Plotter):

    """ Simple plotting script to visualize the output of the MPA Light
    synchronous readout (correlate hit maps with bunch crossing data). """

    def __init__(self, bx, hm):

        """ Initialize class instances. """

        # Get MPA lists from BunchCrossing and HitMap objects
        self._MPAs_bx = bx.get_mpas()
        self._MPAs_hm = hm.get_mpas()

        # Check that both lists have same length
        if len(self._MPAs_bx) != len(self._MPAs_hm):
            raise IndexError('BunchCrossing and HitMap objects have different '
                             'number of MPAs.')

    def plot_cts_bx_px(self, path):

        """ Plots counts vs. bunch crossing separate in each pixel. """

        system('mkdir -p %s' % path)
        name = 'counts_per_bx_MPA%s_px%s'
        x_title = 'BX'
        y_title = 'Event count'

        # Create THStack and its TLegend
        stack = THStack(name % ('all', 'all'), name % ('all', 'all'))
        leg = TLegend(.9, .5, 1., .9)

        for idx_mpa in range(0, len(self._MPAs_bx)):

            # Create THStack and its TLegend
            stack_mpa = THStack(name % (idx_mpa, 'all'), name % (idx_mpa, 'all'))
            leg_mpa = TLegend(.9, .1, 1., .9)

            # List with 48 histograms
            histos = []
            for idx_px in range(0, self._no_pxs_x*self._no_pxs_y):
                histo = TH1F(name % (idx_mpa, idx_px),
                             name % (idx_mpa, idx_px), 100, 0, 100)
                histo.SetLineColor(self._get_color(idx_px))
                histos.append(histo)


            # Remove all 0's from lists
            for idx_shutter in range(0, len(self._MPAs_bx[idx_mpa].get_no_hits_shutter())):
                # Remove all 0's from the lists
                MPA_bx = [val for val in
                          self._MPAs_bx[idx_mpa].get_no_hits_shutter()[idx_shutter]
                          if val != 0]
                MPA_hm = [val for val in
                          self._MPAs_hm[idx_mpa].get_no_hits_shutter()[idx_shutter]
                          if val != 0]

                # Convert hit maps to list of pixels with hits (separately for
                # each hit map)
                MPA_ph = []
                for hit_map in MPA_hm:
                    MPA_ph.append(self._convert(hit_map))

                for idx_hm, MPA_ph_bxs in enumerate(MPA_ph):
                    for MPA_ph_bx in MPA_ph_bxs:
                        histos[MPA_ph_bx].Fill(MPA_bx[idx_hm])

            # Loop over all histos
            for idx_px, histo in enumerate(histos):
                # Add them to stack
                if histo.GetMaximum() != 0.:
                    stack_mpa.Add(histo)
                    leg_mpa.AddEntry(histo, 'px%s' % (idx_px), 'l')
                # Save them
                self._save_histo(histo, '%s/%s.pdf' %
                                 (path, name % (idx_mpa, idx_px)),
                                 x_title, y_title, logy=True,
                                 min=.1, max=20000)

            # Save stack
            if stack_mpa.GetMaximum() != 0.:
                self._save_histo(stack_mpa, '%s/%s.pdf' %
                                 (path, name % (idx_mpa, 'all')),
                                 x_title, y_title, leg_mpa, logy=True,
                                 min=.1, max=20000, draw_option='nostack')

    def _convert(self, MPA_hm):

        """ Convert hit map to list of pixels with hits. """

        MPA_ph = []
        # Reverse loop through hit map digit by digit
        for idx, px in enumerate(str(MPA_hm)[::-1]):
            if px == '1':
                MPA_ph.append(self._get_coordinate(idx))

        return MPA_ph

    def _get_coordinate(self, px):

        """ Get coordinate of pixel, since geometries of hit map and
        calibration differ. """

        if px in range(16, 32):
            return px
        return (47 - px)

    def _get_color(self, px):

        """ Return color for specific pixel. """

        if px == 0:
            return kRed-7
        if px == 1:
            return kPink-7
        if px == 2:
            return kMagenta-7
        if px == 3:
            return kViolet-7
        if px == 4:
            return kBlue-7
        if px == 5:
            return kAzure-7
        if px == 6:
            return kCyan-7
        if px == 7:
            return kTeal-7
        if px == 8:
            return kGreen-7
        if px == 9:
            return kSpring-7
        if px == 10:
            return kYellow-7
        if px == 11:
            return kOrange-7
        if px == 12:
            return kRed-3
        if px == 13:
            return kPink-3
        if px == 14:
            return kMagenta-3
        if px == 15:
            return kViolet-3
        if px == 16:
            return kBlue-3
        if px == 17:
            return kAzure-3
        if px == 18:
            return kCyan-3
        if px == 19:
            return kTeal-3
        if px == 20:
            return kGreen-3
        if px == 21:
            return kSpring-3
        if px == 22:
            return kYellow-3
        if px == 23:
            return kOrange-3
        if px == 24:
            return kRed+2
        if px == 25:
            return kPink+2
        if px == 26:
            return kMagenta+2
        if px == 27:
            return kViolet+2
        if px == 28:
            return kBlue+2
        if px == 29:
            return kAzure+2
        if px == 30:
            return kCyan+2
        if px == 31:
            return kTeal+2
        if px == 32:
            return kGreen+2
        if px == 33:
            return kSpring+2
        if px == 34:
            return kYellow+2
        if px == 35:
            return kOrange+2
        if px == 36:
            return kRed+3
        if px == 37:
            return kPink+3
        if px == 38:
            return kMagenta+3
        if px == 39:
            return kViolet+3
        if px == 40:
            return kBlue+3
        if px == 41:
            return kAzure+3
        if px == 42:
            return kCyan+3
        if px == 43:
            return kTeal+3
        if px == 44:
            return kGreen+3
        if px == 45:
            return kSpring+3
        if px == 46:
            return kYellow+3
        if px == 47:
            return kOrange+3
