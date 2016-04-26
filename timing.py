#!/usr/bin/env python2

""" Author: Basil Schneider <basil.schneider@cern.ch>
Plot different timing delays after receiving the trigger. """

from ROOT import gROOT, TH1F, THStack, TCanvas, TLegend

def get_data(logfile):

    """ Get data from logfile and return list. """

    result = []
    timestamp = logfile[logfile.find('daqout'):].split('_')[3]
    with open('%s/log_%s.log_memory_bx' % (logfile, timestamp), 'r') as f_log:
        for line in f_log:
            result.extend(list(filter(lambda l: l != 0,
                                      [int(x) for x in line.split()])))
    return result

def timing(data, leg_entries):

    """ Plot different timing delays after receiving the trigger. """

    stack = THStack('stack', 'Counts per BX')
    leg = TLegend(.8, .5, 1., .9)
    for idx, list in enumerate(data):
        h = TH1F('', '', 100, 0, 220)
        h.SetFillColor(idx+2)
        leg.AddEntry(h, leg_entries[idx], 'f')
        for val in list:
            h.Fill(val)
        stack.Add(h)
    canvas = TCanvas()
    stack.Draw()
    stack.GetXaxis().SetTitle('BX')
    stack.GetYaxis().SetTitle('Counts')
    leg.Draw()
    canvas.SaveAs('timing.pdf')

if __name__ == '__main__':
    gROOT.SetBatch(True)
    data = []
    leg_entries = ['delay 4 ns', 'delay 40 ns', 'delay 80 ns', 'delay 120 ns',
                   'delay 160 ns', 'delay 200 ns', 'delay 300 ns', 'delay 400 ns',
                   'delay 600 ns', 'delay 1 us', 'delay 1.5 us', 'delay 2 us',
                   'delay 2.5 us', 'delay 3 us', 'delay 3.5 us', 'delay 4 us']
    data.append(get_data('../daqlogs/daqout_default_noprocessing_115325235984_thr90_shdur1e4_nosh1e2_laserEXT_trigdelay4ns'))
    data.append(get_data('../daqlogs/daqout_default_noprocessing_115402963022_thr90_shdur1e4_nosh1e2_laserEXT_trigdelay40ns'))
    data.append(get_data('../daqlogs/daqout_default_noprocessing_115445817427_thr90_shdur1e4_nosh1e2_laserEXT_trigdelay80ns'))
    data.append(get_data('../daqlogs/daqout_default_noprocessing_115530301588_thr90_shdur1e4_nosh1e2_laserEXT_trigdelay120ns'))
    data.append(get_data('../daqlogs/daqout_default_noprocessing_115558063636_thr90_shdur1e4_nosh1e2_laserEXT_trigdelay160ns'))
    data.append(get_data('../daqlogs/daqout_default_noprocessing_115618461435_thr90_shdur1e4_nosh1e2_laserEXT_trigdelay200ns'))
    data.append(get_data('../daqlogs/daqout_default_noprocessing_115727229012_thr90_shdur1e4_nosh1e2_laserEXT_trigdelay300ns'))
    data.append(get_data('../daqlogs/daqout_default_noprocessing_115754263549_thr90_shdur1e4_nosh1e2_laserEXT_trigdelay400ns'))
    data.append(get_data('../daqlogs/daqout_default_noprocessing_115819255012_thr90_shdur1e4_nosh1e2_laserEXT_trigdelay600ns'))
    data.append(get_data('../daqlogs/daqout_default_noprocessing_115844721454_thr90_shdur1e4_nosh1e2_laserEXT_trigdelay1000ns'))
    data.append(get_data('../daqlogs/daqout_default_noprocessing_115907896283_thr90_shdur1e4_nosh1e2_laserEXT_trigdelay1500ns'))
    data.append(get_data('../daqlogs/daqout_default_noprocessing_115939858337_thr90_shdur1e4_nosh1e2_laserEXT_trigdelay2000ns'))
    data.append(get_data('../daqlogs/daqout_default_noprocessing_120013387535_thr90_shdur1e4_nosh1e2_laserEXT_trigdelay2500ns'))
    data.append(get_data('../daqlogs/daqout_default_noprocessing_120036370973_thr90_shdur1e4_nosh1e2_laserEXT_trigdelay3000ns'))
    data.append(get_data('../daqlogs/daqout_default_noprocessing_120100525519_thr90_shdur1e4_nosh1e2_laserEXT_trigdelay3500ns'))
    data.append(get_data('../daqlogs/daqout_default_noprocessing_120124350545_thr90_shdur1e4_nosh1e2_laserEXT_trigdelay4000ns'))
    timing(data, leg_entries)
