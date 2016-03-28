#!/usr/bin/env python2

""" Author: Basil Schneider <basil.schneider@cern.ch>
Simple plotting script to visualize the output of the MPA Light asynchronous
readout (ripple counter). """

from os import system
from ROOT import gROOT, TCanvas, TH1F, THStack, gStyle, TLegend, TH2F
from MPA import MPA
from Geometry import Geometry

class RippleCounter(object):

    """ Simple plotting class to visualize the output of the MPA Light
    asynchronous readout (ripple counter). """

    # Global settings
    _no_mpas = 6
    _no_pxs_x = 16
    _no_pxs_y = 3

    # ROOT batch mode
    gROOT.SetBatch(True)
    # No statistics in plots
    gStyle.SetOptStat(0)

    def __init__(self):

        """ Initialize instances of class. """

        # Create 6 MPA objects
        self._MPAs = []
        for i in range(0, self._no_mpas):
            self._MPAs.append(MPA(self._no_pxs_x*self._no_pxs_y))

    def read_data_raw(self, logfile):

        """ Read in raw logfile and fill MPA objects. """

        # Open raw logfile
        with open(logfile, 'r') as logfile:
            for idx, line in enumerate(logfile):
                # Each line corresponds to one MPA object
                # The correct MPA object is found by idx % len(MPA)
                self._MPAs[idx % len(self._MPAs)].set_no_hits_shutter([int(val) for val
                                                           in line.split()])

    def plot_ripples_shutter(self, path):

        """ Plot ripples vs. shutter. That is one plot per pixel and one for the
        total. """

        system('mkdir -p %s' % path)
        name = 'ripples_per_shutter_px%s_MPA%s'
        x_title = 'Shutter'
        y_title = 'Ripple count'

        # Get number of shutters
        no_shutters = len(self._MPAs[0].get_no_hits_shutter())

        # Create THStack and its TLegend
        stack = THStack(name % ('all', 'all'), name % ('all', 'all'))
        leg = TLegend(.9, .5, 1., .9)

        # Plots for each pixel and each MPA
        for idx_mpa, MPA in enumerate(self._MPAs):

            # Histogram for all pixels on one MPA
            h_mpa = TH1F(name % ('all', idx_mpa), name % ('all', idx_mpa),
                         no_shutters, .5, no_shutters+.5)

            for px in range(0, self._no_pxs_x*self._no_pxs_y):

                # Histogram for one pixel on one MPA
                h_mpa_px = TH1F(name % (px, idx_mpa), name % (px, idx_mpa),
                                 no_shutters, .5, no_shutters+.5)

                for shutter in range(0, no_shutters):
                    h_mpa_px.Fill(shutter+1, MPA.get_no_hits_shutter()[shutter][px])
                    h_mpa.Fill(shutter+1, MPA.get_no_hits_shutter()[shutter][px])

                self._save_histo(h_mpa_px,
                                 '%s/%s.pdf' % (path, name % (px, idx_mpa)),
                                 x_title, y_title)

            self._save_histo(h_mpa,
                             '%s/%s.pdf' % (path, name % ('all', idx_mpa)),
                             x_title, y_title)
            h_mpa.SetFillColor(self._get_fill_color(idx_mpa))
            stack.Add(h_mpa)
            leg.AddEntry(h_mpa, 'MPA%s' % idx_mpa, 'f')

        self._save_histo(stack,
                         '%s/%s.pdf' % (path, name % ('all', 'all')),
                         x_title, y_title, leg)

    def _save_histo(self, histogram, path, x_title='', y_title='',
                    leg=None, draw_option=''):

        """ Plot and save histogram as PDF. """

        canvas = TCanvas()
        histogram.Draw(draw_option)
        histogram.GetXaxis().SetTitle(x_title)
        histogram.GetYaxis().SetTitle(y_title)
        if leg != None:
            leg.Draw()
        canvas.SaveAs(path)

    def _get_fill_color(self, idx):

        """ Return a fill color. """

        return idx+2

    def plot_maps(self, path):

        """ Plot 2d map for specific MPA. """

        system('mkdir -p %s' % path)
        name = 'ripples_maps_MPA%s'

        # Get number of shutters
        no_shutters = len(self._MPAs[0].get_no_hits_shutter())

        # Histogram for all pixels and all MPA's
        map_merged = self._create_map(name % 'merged')

        # List to store map objects for later plotting
        maps = []

        # Plots for each pixel and each MPA
        for idx_mpa, MPA in enumerate(self._MPAs):

            # Define layout of MPA chip
            geometry = Geometry()
            if idx_mpa in [0, 1, 2]:
                geometry.set_geometry([range(32, 48), range(31, 15, -1),
                                       range(0, 16)])
            else:
                geometry.set_geometry([range(15, -1, -1), range(16, 32),
                                       range(47, 31, -1)])

            # Histogram for all pixels on one MPA
            map_mpa = self._create_map(name % idx_mpa)

            for px in range(0, self._no_pxs_x*self._no_pxs_y):

                map_mpa.Fill(geometry.get_x(px), geometry.get_y(px),
                             MPA.get_no_hits()[px])
                map_merged.Fill(geometry.get_x(px), geometry.get_y(px),
                             MPA.get_no_hits()[px])

            maps.append(map_mpa)
            self._save_histo(map_mpa,
                             '%s/%s.pdf' % (path, name % (idx_mpa)),
                             draw_option='COLZ')

        self._save_histo(map_merged,
                         '%s/%s.pdf' % (path, name % ('merged')),
                         draw_option='COLZ')

        self._plot_map_all(maps, path, name)

    def _plot_map_all(self, maps, path, name):

        """ Plot all maps in one TCanvas. """

        canvas = TCanvas()
        canvas.Divide(3, 2)

        for idx, map in enumerate(maps):
            canvas.cd(self._get_mpa_coordinate(idx))
            map.SetTitle('')
            map.Draw('COLZ')

        canvas.SaveAs('%s/%s.pdf' % (path, name % ('all')))

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

    def _create_map(self, name):

        """ Create and return TH2F map. """

        map = TH2F(name, name,
                   self._no_pxs_x, 0, self._no_pxs_x,
                   self._no_pxs_y, 0, self._no_pxs_y)

        # Set number of ticks on x and y axes
        map.GetXaxis().SetNdivisions(self._no_pxs_x, 0, 0)
        map.GetYaxis().SetNdivisions(self._no_pxs_y, 0, 0)

        return map
