#!/usr/bin/env python2

""" Author: Basil Schneider <basil.schneider@cern.ch>
Simple plotting script to visualize the output of the MPA Light synchronous
readout (bunch crossing data). """

from Plotter import Plotter

class BunchCrossing(Plotter):

    """ Simple plotting class to visualize the output of the MPA Light
    synchronous readout (bunch crossing data). """

    def __init__(self):

        """ Initialize class instances. """

        self._initialize_mpas(self._no_mems)
