#!/usr/bin/env python2

""" Author: Basil Schneider <basil.schneider@cern.ch>
Get plots from MPA measurements. """

from RippleCounter import RippleCounter
from BunchCrossing import BunchCrossing
from HitMap import HitMap

if __name__ == '__main__':

    rc = RippleCounter()

    # Define where to get the logfiles
    #path_timestamp = '112132256811'
    #path_logs = '/home/bschneid/MAPSA_Software/daqlogs/'
    #path_logs+= 'daqout_default_noprocessing_%s_none/' % path_timestamp
    path_logs = '/home/bschneid/MAPSA_Software/daqlogs/daqout_default_noprocessing_143334709341_thr80_sh5000_nosh100_laserON'
    path_timestamp = '143334709341'

    # Read in data from raw log file and store it in MPA object
    rc.read_data_raw('%s/log_%s.log_counter' % (path_logs, path_timestamp))

    # Plot ripples vs. shutter
    rc.plot_ripples_shutter('%s/plots/ripples_per_shutter/' % path_logs)

    # Plot 2d maps
    rc.plot_maps('%s/plots/ripples_maps/' % path_logs)

    bx = BunchCrossing()

    # Read in data from raw log file and store it in MPA object
    bx.read_data_raw('%s/log_%s.log_memory_bx' % (path_logs, path_timestamp))

    # Plot counts vs. bunch crossing
    bx.plot_cts_bx('%s/plots/counts_per_bx/' % path_logs)

    hm = HitMap()

    # Read in data from raw log file and store it in MPA object
    hm.read_data_raw('%s/log_%s.log_memory_data' % (path_logs, path_timestamp))

    # Plot hit maps
    hm.plot_maps('%s/plots/hit_maps/' % path_logs)
