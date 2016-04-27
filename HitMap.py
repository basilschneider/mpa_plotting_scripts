#!/usr/bin/env python2

""" Author: Basil Schneider <basil.schneider@cern.ch>
Simple plotting script to visualize the output of the MPA Light synchronous
readout (hit map data). """

from os import system
from ROOT import TH2F, TCanvas
from Plotter import Plotter
from Geometry import Geometry

class HitMap(Plotter):

    """ Simple plotting class to visualize the output of the MPA Light
    synchronous readout (hit map data). """

    def __init__(self):

        """ Initialize class instances. """

        self._initialize_mpas(self._no_mems)

    def plot_maps(self, path):

        """ Plot 2d hit map for specific MPA. """

        system('mkdir -p %s' % path)
        name = 'hit_maps_MPA%s'

        # Get number of shutters
        no_shutters = len(self._MPAs[0].get_no_hits_shutter())

        # Histogram for all pixels and all MPA's
        map_merged = self._create_map(name % 'merged')

        # List to store map objects for later plotting
        maps = []

        # Find maximum Z for adjusting Z range later
        z_max = 0

        # Plots for each pixel and each MPA
        for idx_mpa, MPA in enumerate(self._MPAs):

            # Define layout of MPA chip (this layout is different from the
            # ripple counter layout, since the data is stored in a different
            # way (empirical fact))
            geometry = Geometry()
            geometry.set_geometry([range(32, 48), range(31, 15, -1),
                                   range(0, 16)])

            # Histogram for all pixels on one MPA
            map_mpa = self._create_map(name % idx_mpa)

            for i_hit_maps in MPA.get_no_hits_shutter():
                for i_hit_map in i_hit_maps:

                    s_hit_map = str(i_hit_map).zfill(self._no_pxs_x*self._no_pxs_y)

                    for px, px_hits in enumerate(s_hit_map):
                        map_mpa.Fill(geometry.get_x(px), geometry.get_y(px),
                                     float(px_hits))
                        map_merged.Fill(geometry.get_x(px), geometry.get_y(px),
                                        float(px_hits))

            # For the map showing all MPA's we want the Z range to be the same
            # Find maximum here
            z_max = max(z_max, map_mpa.GetMaximum())

            maps.append(map_mpa)
            self._save_histo(map_mpa,
                             '%s/%s.pdf' % (path, name % (idx_mpa)),
                             draw_option='COLZ')

        self._save_histo(map_merged,
                         '%s/%s.pdf' % (path, name % ('merged')),
                         draw_option='COLZ')

        self._plot_map_all(maps, path, name, z_max)

    def _plot_map_all(self, maps, path, name, z_max):

        """ Plot all maps in one TCanvas. """

        canvas = TCanvas()
        canvas.Divide(3, 2)

        for idx, map in enumerate(maps):
            canvas.cd(self._get_mpa_coordinate(idx))
            map.GetZaxis().SetRangeUser(0., z_max)
            map.SetTitle('')
            if idx in [2, 3]:
                drawing_option = 'COLZ'
            else:
                drawing_option = 'COL'
            # Draw also text
            drawing_option += '|TEXT90'
            map.SetMarkerSize(1.7)
            map.Draw(drawing_option)

        canvas.SaveAs('%s/%s.pdf' % (path, name % ('all')))

    def _create_map(self, name):

        """ Create and return TH2F map. """

        map = TH2F(name, name,
                   self._no_pxs_x, 0, self._no_pxs_x,
                   self._no_pxs_y, 0, self._no_pxs_y)

        # Set number of ticks on x and y axes
        map.GetXaxis().SetNdivisions(self._no_pxs_x, 0, 0)
        map.GetYaxis().SetNdivisions(self._no_pxs_y, 0, 0)

        return map
