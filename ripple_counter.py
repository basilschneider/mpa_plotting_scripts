#!/usr/bin/env python2

""" Author: Basil Schneider <basil.schneider@cern.ch>
Simple plotting script to visualize the output of the MPA Light asynchronous
readout (ripple counter. """

from os import system
from ROOT import gROOT, TCanvas, TH1F
from MPA import MPA

NO_MPAS = 6
NO_PXS = 48

def read_data_raw(logfile, MPAs):

    """ Read in raw logfile and fill MPA objects. """

    # Open raw logfile
    with open(logfile, 'r') as logfile:
        for idx, line in enumerate(logfile):
            # Each line corresponds to one MPA object
            # The correct MPA object is found by idx % len(MPA)
            MPAs[idx % len(MPAs)].set_no_hits_shutter([int(val) for val
                                                       in line.split()])

def plot_ripples_shutter(MPAs, path):

    """ Plot ripples vs. shutter. That is one plot per pixel and one for the
    total. """

    system('mkdir -p %s' % path)
    name = 'ripples_per_shutter_px%s_MPA%s'
    x_title = 'Shutter'
    y_title = 'Ripple count'

    # Get number of shutters
    no_shutters = len(MPAs[0].get_no_hits_shutter())

    # Plots for each pixel and each MPA
    for idx, MPA in enumerate(MPAs):

        # Histogram for all pixels on one MPA
        h_mpa = TH1F(name % ('all', idx), name % ('all', idx),
                     no_shutters, .5, no_shutters+.5)

        for px in range(0, NO_PXS):

            # Histogram for one pixel on one MPA
            h_mpa_px = TH1F(name % (px, idx), name % (px, idx),
                             no_shutters, .5, no_shutters+.5)
            for shutter in range(0, no_shutters):
                h_mpa_px.Fill(shutter+1, MPA.get_no_hits_shutter()[shutter][px])
                h_mpa.Fill(shutter+1, MPA.get_no_hits_shutter()[shutter][px])

            save_histo(h_mpa_px, x_title, y_title,
                       '%s/%s.pdf' % (path, name % (px, idx)))

        save_histo(h_mpa, x_title, y_title,
                   '%s/%s.pdf' % (path, name % ('all', idx)))

def save_histo(histogram, x_title, y_title, path):

    """ Plot and save histogram as PDF. """

    canvas = TCanvas()
    histogram.Draw()
    histogram.GetXaxis().SetTitle(x_title)
    histogram.GetYaxis().SetTitle(y_title)
    canvas.SaveAs(path)

if __name__ == '__main__':

    # ROOT batch mode
    gROOT.SetBatch(True)

    # Create 6 MPA objects
    MPAs = []
    for i in range(0, NO_MPAS):
        MPAs.append(MPA(NO_PXS))

    # Define where to get the logfiles
    path_timestamp = '112132256811'
    path_logs = '/home/bschneid/MAPSA_Software/daqlogs/'
    path_logs+= 'daqout_default_noprocessing_%s_none/' % path_timestamp

    # Read in data from raw log file and store it in MPA object
    read_data_raw('%s/log_%s.log_counter' % (path_logs, path_timestamp), MPAs)

    # Plot ripples vs. shutter
    plot_ripples_shutter(MPAs, '%s/plots/ripples_per_shutter/' % path_logs)

    for MPA in MPAs:
        print MPA
        for shutter in MPA.get_no_hits_shutter():
            print shutter
