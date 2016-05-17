#!/usr/bin/env python2

""" Author: Basil Schneider <basil.schneider@cern.ch>
Get plots from MPA measurements. """

from sys import argv
from os import mkdir
from glob import glob
from ROOT import TH1F, TH2F, TCanvas, TLegend
from ROOT import kRed, kViolet, kBlue, kGreen, kPink, kMagenta
from RippleCounter import RippleCounter
from BunchCrossing import BunchCrossing
from HitMap import HitMap
from SynchronousData import SynchronousData

def set_style_color(histo, idx):
    if idx == 0:
        histo.SetLineColor(kRed)
    if idx == 1:
        histo.SetLineColor(kViolet)
    if idx == 2:
        histo.SetLineColor(kBlue)
    if idx == 3:
        histo.SetLineColor(kGreen+2)
    if idx == 4:
        histo.SetLineColor(kPink+7)
    if idx == 5:
        histo.SetLineColor(kMagenta+4)
    if 'px23' in histo.GetName():
        histo.SetLineStyle(6)

if __name__ == '__main__':

    mpa_plot = 4
    pxs_plot = [22, 23]
    bxs_plot = [8, 9, 10, 11]

    # Plot parameters
    microstep = .047625
    no_bins_x = 30
    bin_lo_x = -50*microstep
    bin_hi_x = 2950*microstep
    no_bins_y = len(bxs_plot)
    bin_lo_y = min(bxs_plot)-.5
    bin_hi_y = max(bxs_plot)+.5
    no_bins_y_eff = 13
    bin_lo_y_eff = -2
    bin_hi_y_eff = 50
    n = 1000.
    canvas = TCanvas()

    titleeff2d22 = 'effs_2d_px22'
    histoeff2d22 = TH2F(titleeff2d22, titleeff2d22,
                      no_bins_x, bin_lo_x, bin_hi_x,
                      no_bins_y_eff, bin_lo_y_eff, bin_hi_y_eff)

    titleeff2d23 = 'effs_2d_px23'
    histoeff2d23 = TH2F(titleeff2d23, titleeff2d23,
                      no_bins_x, bin_lo_x, bin_hi_x,
                      no_bins_y_eff, bin_lo_y_eff, bin_hi_y_eff)

    for arg in argv[1:]:

        # Get the path's to the logs
        glob_logs = arg
        path_logs = glob('../daqlogs/*{0}*'.format(glob_logs))

        hms = []
        bxs = []
        rcs = []
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

            # Initialize Ripple Counter objects
            rc = RippleCounter()
            rc.read_data_raw('%s/log_%s.log_counter' % (path_log, path_timestamp))

            rcs.append(rc)

        # Print out some information about data for debugging
        # (limit print out to 12 elements, since it's too much information otherwise)
        #for idx, path_log in enumerate(path_logs):
        #    cor_x = int(path_log.split('_')[-1].lstrip('x')) + 600
        #    print 'Coordinate X:', cor_x
        #    print 'HMS'
        #    print len(hms[idx].get_mpas()[mpa_plot].get_no_hits_shutter())
        #    print hms[idx].get_mpas()[mpa_plot].get_no_hits_shutter()[:12]
        #    print 'BXS'
        #    print len(bxs[idx].get_mpas()[mpa_plot].get_no_hits_shutter())
        #    print bxs[idx].get_mpas()[mpa_plot].get_no_hits_shutter()[:12]
        #    print 'RCS'
        #    print rcs[idx].get_mpas()[mpa_plot].get_no_hits()

        titleall = 'cts_vs_x_bxall_pxall'
        histoall = TH1F(titleall, titleall, no_bins_x, bin_lo_x, bin_hi_x)

        titleasyncall = 'cts_vs_x_async_bxall_pxall'
        histoasyncall = TH1F(titleasyncall, titleasyncall, no_bins_x, bin_lo_x, bin_hi_x)

        l_effs_bx = []
        l_effs = []
        l_effa = []
        l_effs_effa = []

        mkdir(arg)

        for px_plot in pxs_plot:
            titlepx = 'cts_vs_x_bxall_px{0}'.format(px_plot)
            histopx = TH1F(titlepx, titlepx, no_bins_x, bin_lo_x, bin_hi_x)

            titlepxeff = 'effs_vs_x_bxall_px{0}'.format(px_plot)
            histopxeff = TH1F(titlepxeff, titlepxeff, no_bins_x, bin_lo_x, bin_hi_x)

            titlepxeffdiv = 'effs_vs_x_bxall_px{0}_div'.format(px_plot)
            histopxeffdiv = TH1F(titlepxeffdiv, titlepxeffdiv, no_bins_x, bin_lo_x, bin_hi_x)

            titleasyncpx = 'cts_vs_x_async_bxall_px{0}'.format(px_plot)
            histoasyncpx = TH1F(titleasyncpx, titleasyncpx, no_bins_x, bin_lo_x, bin_hi_x)

            titleasyncpxeff = 'effs_px{0}'.format(px_plot)
            histoasyncpxeff = TH1F(titleasyncpxeff, titleasyncpxeff, no_bins_x, bin_lo_x, bin_hi_x)

            title2px = 'cts_vs_bx_vs_x_px{0}'.format(px_plot)
            histo2px = TH2F(title2px, title2px, no_bins_x, bin_lo_x, bin_hi_x,
                            no_bins_y, bin_lo_y, bin_hi_y)

            for idx_bx, bx_plot in enumerate(bxs_plot):

                title = 'cts_vs_x_bx{0}_px{1}'.format(bx_plot, px_plot)
                histo = TH1F(title, title, no_bins_x, bin_lo_x, bin_hi_x)

                titleeff = 'effs_vs_x_bx{0}_px{1}'.format(bx_plot, px_plot)
                histoeff = TH1F(titleeff, titleeff, no_bins_x, bin_lo_x, bin_hi_x)

                for idx_log, path_log in enumerate(path_logs):
                    # Find the x position, this is hardcoded for now
                    #cor_x = int(path_log.split('_')[-1].lstrip('x')) + 600
                    cor_x = int(path_log.split('X')[1].split('_')[0]) - 917000
                    cor_x *= microstep

                    # Find the delay, this is hardcoded for now
                    delay = float(path_log.split('to')[1].split('ns')[0])

                    # Fill async plots (independent of BX's)
                    if idx_bx == 0:
                        histoasyncpx.Fill(cor_x, rcs[idx_log].get_mpas()[mpa_plot]
                                          .get_no_hits()[px_plot])
                        histoasyncall.Fill(cor_x, rcs[idx_log].get_mpas()[mpa_plot]
                                           .get_no_hits()[px_plot])
                        histoasyncpxeff.Fill(cor_x, (rcs[idx_log].get_mpas()[mpa_plot]
                                             .get_no_hits()[px_plot])/n)

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
                                        histoeff.Fill(cor_x, 1./n)
                                        histoall.Fill(cor_x)
                                        histopx.Fill(cor_x)
                                        histopxeff.Fill(cor_x, 1./n)
                                        histopxeffdiv.Fill(cor_x, 1./n)
                                        histo2px.Fill(cor_x, bxs_shutter[idx_clk])
                                        if hm_shutter == 22:
                                            histoeff2d22.Fill(cor_x, delay, 1./n)
                                        if hm_shutter == 23:
                                            histoeff2d23.Fill(cor_x, delay, 1./n)

                canvas.cd()
                histo.Draw()
                histo.SetTitle('Occupancy for pixel {0} in BX {1}'.format(px_plot, bx_plot))
                histo.GetXaxis().SetTitle('x [#mum]')
                histo.GetYaxis().SetTitle('Counts')
                canvas.Print('{0}/{1}.pdf'.format(arg, title))
                canvas.Clear()

                if histoeff.Integral() > 0.:
                    l_effs_bx.append(histoeff)

            canvas.cd()
            histopx.Draw()
            histopx.SetTitle('Occupancy for pixel {0} in all BX\'s'.format(px_plot))
            histopx.GetXaxis().SetTitle('x [#mum]')
            histopx.GetYaxis().SetTitle('Counts')
            canvas.Print('{0}/{1}.pdf'.format(arg, titlepx))
            canvas.Clear()

            if histopxeff.Integral() > 0.:
                l_effs.append(histopxeff)

            canvas.cd()
            histoasyncpx.Draw()
            histoasyncpx.SetTitle('Occupancy for pixel {0} (async readout)'.format(px_plot))
            histoasyncpx.GetXaxis().SetTitle('x [#mum]')
            histoasyncpx.GetYaxis().SetTitle('Counts')
            canvas.Print('{0}/{1}.pdf'.format(arg, titleasyncpx))
            canvas.Clear()

            if histoasyncpxeff.Integral() > 0.:
                l_effa.append(histoasyncpxeff)

            histopxeffdiv.Divide(histoasyncpxeff)
            if histopxeffdiv.Integral() > 0.:
                l_effs_effa.append(histopxeffdiv)

            canvas.cd()
            histo2px.Draw('COLZ')
            histo2px.SetTitle('Occupancy for pixel {0} in all BX\'s'.format(px_plot))
            histo2px.GetXaxis().SetTitle('x [#mum]')
            histo2px.GetYaxis().SetTitle('BX')
            histo2px.GetZaxis().SetTitle('assdafasf')
            canvas.Print('{0}/{1}.pdf'.format(arg, title2px))
            canvas.Clear()

        canvas.cd()
        histoall.Draw()
        histoall.SetTitle('Occupancy for all pixels in all BX\'s')
        histoall.GetXaxis().SetTitle('x [#mum]')
        histoall.GetYaxis().SetTitle('Counts')
        canvas.Print('{0}/{1}.pdf'.format(arg, titleall))
        canvas.Clear()

        canvas.cd()
        histoasyncall.Draw()
        histoasyncall.SetTitle('Occupancy for all pixels (async readout)')
        histoasyncall.GetXaxis().SetTitle('x [#mum]')
        histoasyncall.GetYaxis().SetTitle('Counts')
        canvas.Print('{0}/{1}.pdf'.format(arg, titleasyncall))
        canvas.Clear()

        del histoall, histoasyncall

        # Plot synchronous efficiencies (per bx)
        leg = TLegend(.9, .5, 1., .9)
        for idx, histo in enumerate(l_effs_bx):

            set_style_color(histo, idx)

            if idx == 0:
                same = ''
                histo.SetTitle('#epsilon_{s} = #hits_{sync}/n')
                histo.GetXaxis().SetTitle('x [#mum]')
                histo.GetYaxis().SetTitle('Counts')
                histo.SetMaximum(1.05)
            else:
                same = 'SAME'

            histo.Draw(same)
            title = ' '.join(histo.GetName().split('_')[-2:])
            leg.AddEntry(histo, title, 'l')

        leg.Draw()
        canvas.Print('{0}/{1}.pdf'.format(arg, 'effs_vs_x_bx_lin'))
        canvas.SetLogy()
        canvas.Print('{0}/{1}.pdf'.format(arg, 'effs_vs_x_bx_log'))
        canvas.Clear()
        canvas.SetLogy(0)

        # Plot synchronous efficiencies (all bx)
        leg = TLegend(.9, .5, 1., .9)
        for idx, histo in enumerate(l_effs):

            set_style_color(histo, idx)

            if idx == 0:
                same = ''
                histo.SetTitle('#epsilon_{s} = #hits_{sync}/n')
                histo.GetXaxis().SetTitle('x [#mum]')
                histo.GetYaxis().SetTitle('Counts')
                histo.SetMaximum(1.05)
            else:
                same = 'SAME'

            histo.Draw(same)
            title = ' '.join(histo.GetName().split('_')[-1:])
            leg.AddEntry(histo, title, 'l')

        leg.Draw()
        canvas.Print('{0}/{1}.pdf'.format(arg, 'effs_vs_x_lin'))
        canvas.SetLogy()
        canvas.Print('{0}/{1}.pdf'.format(arg, 'effs_vs_x_log'))
        canvas.Clear()
        canvas.SetLogy(0)

        # Plot asynchronous efficiencies
        leg = TLegend(.9, .5, 1., .9)
        for idx, histo in enumerate(l_effa):

            set_style_color(histo, idx)

            if idx == 0:
                same = ''
                histo.SetTitle('#epsilon_{a} = #hits_{async}/n')
                histo.GetXaxis().SetTitle('x [#mum]')
                histo.GetYaxis().SetTitle('Counts')
                histo.SetMaximum(1.05)
            else:
                same = 'SAME'

            histo.Draw(same)
            title = ' '.join(histo.GetName().split('_')[-1:])
            leg.AddEntry(histo, title, 'l')

        leg.Draw()
        canvas.Print('{0}/{1}.pdf'.format(arg, 'effa_vs_x_lin'))
        canvas.SetLogy()
        canvas.Print('{0}/{1}.pdf'.format(arg, 'effa_vs_x_log'))
        canvas.Clear()
        canvas.SetLogy(0)

        # Divide efficiencies sync by async
        leg = TLegend(.9, .5, 1., .9)
        for idx, histo in enumerate(l_effs_effa):

            # Check for bins above 1
            for bin in range(0, histo.GetNbinsX()+2):
                if histo.GetBinContent(bin) > 1.:
                    print 'Found bin with more hits in synchronous',
                    print 'readout as in asynchronous readout.',
                    print 'Bin content is %s' % (histo.GetBinContent(bin))

            set_style_color(histo, idx)

            if idx == 0:
                same = ''
                histo.SetTitle('#epsilon_{s}/#epsilon_{a}')
                histo.GetXaxis().SetTitle('x [#mum]')
                histo.GetYaxis().SetTitle('Counts')
                histo.SetMaximum(1.05)
            else:
                same = 'SAME'

            histo.Draw(same)
            title = histo.GetName().split('_')[-2]
            leg.AddEntry(histo, title, 'l')

        leg.Draw()
        canvas.Print('{0}/{1}.pdf'.format(arg, 'effs_effa_lin'))
        canvas.SetLogy()
        canvas.Print('{0}/{1}.pdf'.format(arg, 'effs_effa_log'))
        canvas.Clear()
        canvas.SetLogy(0)

    canvas.cd()
    histoeff2d22.Draw('COLZ')
    histoeff2d22.SetTitle('#epsilon_{s}')
    histoeff2d22.GetXaxis().SetTitle('x [#mum]')
    histoeff2d22.GetYaxis().SetTitle('delay [ns]')
    canvas.Print('{0}.pdf'.format(titleeff2d22))
    canvas.Clear()

    canvas.cd()
    histoeff2d23.Draw('COLZ')
    histoeff2d23.SetTitle('#epsilon_{s}')
    histoeff2d23.GetXaxis().SetTitle('x [#mum]')
    histoeff2d23.GetYaxis().SetTitle('delay [ns]')
    canvas.Print('{0}.pdf'.format(titleeff2d23))
    canvas.Clear()

