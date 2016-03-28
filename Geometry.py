#!/usr/bin/env python2

""" Author: Basil Schneider <basil.schneider@cern.ch>
Define 2d geometry of MPA devices. """

class Geometry(object):

    def __init__(self):

        """ Initialize instances of class. """

        self._geometry = []
        self._bins_x = 0
        self._bins_y = 0

    def set_geometry(self, geometry):

        """ Defines geometry, i.e. the following list is interpreted as a
        geometry:

        [[1, 2, 3][4, 5, 6]]

        1 2 3
        4 5 6"""

        # Set geometry
        self._geometry = geometry

        # Get number of bins in x
        self._bins_x = 0
        for subgeometry in geometry:
            self._bins_x = max(self._bins_x, len(subgeometry))

        # Get number of bins in y
        self._bins_y = len(geometry)

    def get_x(self, numbering):

        """ Return x axis coordinate in TH2F for numbering. """

        for subgeometry in self._geometry:
            if numbering in subgeometry:
                return subgeometry.index(numbering) + 0.5

    def get_y(self, numbering):

        """ Return y axis coordinate in TH2F for numbering. """

        for idx, subgeometry in enumerate(self._geometry):
            if numbering in subgeometry:
                # Subtract idx from number of bins in y, since we start
                # counting from top; subtract 0.5 to hit bin center
                return self._bins_y - idx - 0.5
