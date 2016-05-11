#!/usr/bin/env python2

""" Author: Basil Schneider <basil.schneider@cern.ch>
Get plots from MPA measurements. """

from sys import argv
from RippleCounter import RippleCounter
from BunchCrossing import BunchCrossing
from HitMap import HitMap
from SynchronousData import SynchronousData

if __name__ == '__main__':

    # Get the path to the logs
    path_logs = argv[1]
    # Need timestamp from path, this method is not foolproof!
    path_timestamp = path_logs[path_logs.find('daqout'):].split('_')[3]

    rc = RippleCounter()

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

    sd = SynchronousData(bx, hm)

    # Plot counts vs. bunch crossing separate for each pixel
    sd.plot_cts_bx_px('%s/plots/counts_per_px_bx' % path_logs)
