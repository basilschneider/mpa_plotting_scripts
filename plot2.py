#!/usr/bin/env python2

""" Author: Basil Schneider <basil.schneider@cern.ch>
Get plots from MPA measurements. """

from sys import argv
from glob import glob
from ROOT import TH1F, TH2F, TCanvas
from RippleCounter import RippleCounter
from BunchCrossing import BunchCrossing
from HitMap import HitMap
from SynchronousData import SynchronousData

if __name__ == '__main__':

    mpa_plot = 4
    pxs_plot = [27, 28]
    bxs_plot = [7, 8, 9, 10]

    # Get the path's to the logs
    glob_logs = argv[1]
    path_logs = glob('../daqlogs/*{0}*'.format(glob_logs))

    hms = []
    bxs = []
    for path_log in path_logs:
        # Need timestamp from path, this method is not foolproof!
        path_timestamp = path_log[path_log.find('daqout'):].split('_')[3]

        # Initialize Hit Map objects
        hm = HitMap()
        hm.read_data_raw('%s/log_%s.log_memory_data' %
                         (path_log, path_timestamp))

        for mpa in hm.get_mpas():
            # Get rid of all 0's in data
            mpa.trim_no_hits_shutter()

            # Convert hit maps to list of pixels with hits
            mpa.convert_hm_to_px()


        hms.append(hm)

        # Initialize Bunch Crossing objects
        bx = BunchCrossing()
        bx.read_data_raw('%s/log_%s.log_memory_bx' %
                         (path_log, path_timestamp))

        # Get rid of all 0's in data
        for mpa in bx.get_mpas():
            mpa.trim_no_hits_shutter()

        bxs.append(bx)

    ## Print out some information about data for debugging
    #for idx, path_log in enumerate(path_logs):
    #    cor_x = int(path_log.split('_')[-1].lstrip('x')) + 600
    #    print 'Coordinate X:', cor_x
    #    print 'HMS'
    #    print len(hms[idx].get_mpas()[mpa_plot].get_no_hits_shutter())
    #    print hms[idx].get_mpas()[mpa_plot].get_no_hits_shutter()[:12]
    #    print 'BXS'
    #    print len(bxs[idx].get_mpas()[mpa_plot].get_no_hits_shutter())
    #    print bxs[idx].get_mpas()[mpa_plot].get_no_hits_shutter()[:12]

    # Plot counts vs x for given BX
    no_bins_x = len(path_logs)
    bin_lo_x = -25
    bin_hi_x = 625
    no_bins_y = len(bxs_plot)
    bin_lo_y = min(bxs_plot)-.5
    bin_hi_y = max(bxs_plot)+.5

    titleall = 'cts_vs_x_bxall_pxall'
    histoall = TH1F(titleall, titleall, no_bins_x, bin_lo_x, bin_hi_x)
    canvas = TCanvas()

    for px_plot in pxs_plot:
        titlepx = 'cts_vs_x_bxall_px{0}'.format(px_plot)
        histopx = TH1F(titlepx, titlepx, no_bins_x, bin_lo_x, bin_hi_x)

        title2px = 'cts_vs_bx_vs_x_px{0}'.format(px_plot)
        histo2px = TH2F(title2px, title2px, no_bins_x, bin_lo_x, bin_hi_x,
                        no_bins_y, bin_lo_y, bin_hi_y)

        for bx_plot in bxs_plot:

            title = 'cts_vs_x_bx{0}_px{1}'.format(bx_plot, px_plot)
            histo = TH1F(title, title, no_bins_x, bin_lo_x, bin_hi_x)

            for idx_log, path_log in enumerate(path_logs):
                # Find the x position, this is mostly hardcoded for now
                cor_x = int(path_log.split('_')[-1].lstrip('x')) + 600

                for idx_shutter in range(0, len(bxs[idx_log].get_mpas()[mpa_plot]
                                                .get_no_hits_shutter())):
                    bxs_shutter = \
                        bxs[idx_log].get_mpas()[mpa_plot].get_no_hits_shutter()[idx_shutter]
                    hms_shutter = \
                        hms[idx_log].get_mpas()[mpa_plot].get_no_hits_shutter()[idx_shutter]

                    for idx_clk in range(0, len(bxs_shutter)):
                        if bxs_shutter[idx_clk] == bx_plot:
                            for hm_shutter in hms_shutter[idx_clk]:
                                if hm_shutter == px_plot:
                                    histo.Fill(cor_x)
                                    histoall.Fill(cor_x)
                                    histopx.Fill(cor_x)
                                    histo2px.Fill(cor_x, bxs_shutter[idx_clk])

            histo.Draw()
            histo.SetTitle('Occupancy for pixel {0} in BX {1}'.format(px_plot, bx_plot))
            histo.GetXaxis().SetTitle('x position')
            histo.GetYaxis().SetTitle('Counts')
            canvas.Print('{0}.pdf'.format(title))

        histopx.Draw()
        histopx.SetTitle('Occupancy for pixel {0} in all BX\'s'.format(px_plot))
        histopx.GetXaxis().SetTitle('x position')
        histopx.GetYaxis().SetTitle('Counts')
        canvas.Print('{0}.pdf'.format(titlepx))

        histo2px.Draw('COLZ')
        histo2px.SetTitle('Occupancy for pixel {0} in all BX\'s'.format(px_plot))
        histo2px.GetXaxis().SetTitle('x position')
        histo2px.GetYaxis().SetTitle('BX')
        histo2px.GetZaxis().SetTitle('assdafasf')
        canvas.Print('{0}.pdf'.format(title2px))

    histoall.Draw()
    histoall.SetTitle('Occupancy for all pixels in all BX\'s')
    histoall.GetXaxis().SetTitle('x position')
    histoall.GetYaxis().SetTitle('Counts')
    canvas.Print('{0}.pdf'.format(titleall))

    ## Get the path to the logs
    #path_logs = argv[1]
    ## Need timestamp from path, this method is not foolproof!
    #path_timestamp = path_logs[path_logs.find('daqout'):].split('_')[3]

    #rc = RippleCounter()

    ## Read in data from raw log file and store it in MPA object
    #rc.read_data_raw('%s/log_%s.log_counter' % (path_logs, path_timestamp))

    ## Plot ripples vs. shutter
    #rc.plot_ripples_shutter('%s/plots/ripples_per_shutter/' % path_logs)

    ## Plot 2d maps
    #rc.plot_maps('%s/plots/ripples_maps/' % path_logs)

    #bx = BunchCrossing()

    ## Read in data from raw log file and store it in MPA object
    #bx.read_data_raw('%s/log_%s.log_memory_bx' % (path_logs, path_timestamp))

    ## Plot counts vs. bunch crossing
    #bx.plot_cts_bx('%s/plots/counts_per_bx/' % path_logs)

    #hm = HitMap()

    ## Read in data from raw log file and store it in MPA object
    #hm.read_data_raw('%s/log_%s.log_memory_data' % (path_logs, path_timestamp))

    ## Plot hit maps
    ##hm.plot_maps('%s/plots/hit_maps/' % path_logs)

    #sd = SynchronousData(bx, hm)

    ## Plot counts vs. bunch crossing separate for each pixel
    #sd.plot_cts_bx_px('%s/plots/counts_per_px_bx' % path_logs)
