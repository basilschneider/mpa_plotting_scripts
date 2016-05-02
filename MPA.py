#!/usr/bin/env python2

""" Author: Basil Schneider <basil.schneider@cern.ch>
MPA data class to store MPA specific quantitites. """

from itertools import izip

class MPA(object):

    """ MPA data class to store MPA specific qantitities. The data is stored in
    _no_hits_shutter. This is a list of list with the following structure:
    [[a,b,...], [c,d], ...] - a is the no. of hits on pixel 1 during shutter 1
                              b is the no. of hits on pixel 2 during shutter 1
                              c is the no. of hits on pixel 1 during shutter 2
                              d is the no. of hits on pixel 2 during shutter 2
                              ...
    """

    def __init__(self, no_elements):

        """ Initialize instances. """

        # Number of elements in lists
        # This corresponds to number of pixels for asynchronous readout and
        # number of words for synchronous readout
        self.no_elements = no_elements

        # Number of hits per shutter
        self._no_hits_shutter = []

    def set_no_hits_shutter(self, no_hits):

        """ Set number of hits per shutter. """

        self.check_if_list(no_hits, self.no_elements, self.no_elements)
        self._no_hits_shutter.append(no_hits)

    def get_no_hits_shutter(self):

        """ Get number of hits per shutter. """

        return self._no_hits_shutter

    def trim_no_hits_shutter(self):

        """ Remove all 0's in hits per shutter data. """

        # Get rid of all 0's in the sublists
        self._no_hits_shutter = [[val for val in sublist if val != 0]
                                 for sublist in self.get_no_hits_shutter()]
        # Get rid of all empty sublists
        self._no_hits_shutter = [sublist for sublist
                                 in self.get_no_hits_shutter()
                                 if len(sublist) > 0]

    def convert_hm_to_px(self):

        """ Convert hit maps to list of pixels with hits. """

        MPA_ph = []
        for hit_map_list in self._no_hits_shutter:
            MPA_ph_shutter = []
            for hit_map in hit_map_list:
                MPA_ph_shutter_bx = []
                # Reverse loop through hit map digit by digit
                for idx, px in enumerate(str(hit_map)[::-1]):
                    if px == '1':
                        MPA_ph_shutter_bx.append(self._get_coordinate(idx))
                MPA_ph_shutter.append(MPA_ph_shutter_bx)
            MPA_ph.append(MPA_ph_shutter)

        self._no_hits_shutter = MPA_ph

    def _get_coordinate(self, px):

        """ Get coordinate of pixel, since geometries of hit map and
        calibration differ. """

        if px in range(16, 32):
            return px
        return (47 - px)

    def get_no_hits(self):

        """ Get number of hits, integrated over all shutters. """

        return [sum(sublist) for sublist in izip(*self.get_no_hits_shutter())]

    def get_max(self):

        """ Get highest value in self._no_hits_shutter. """

        max_value = 0
        for element in self._no_hits_shutter:
            max_value = max(max_value, max(element))

        return max_value

    def check_if_list(self, lst, length_min=-1, length_max=-1):

        """ Check if user passed a list and if meets the requirements of
        minimum and maximum lengths. """

        # Check if it is a list
        if not isinstance(lst, list):
            raise TypeError('The object %s is not of type %s.'
                            % (obj, obj_type.__name__))

        # Check for the minimum length of the list
        if length_min > -1 and len(lst) < length_min:
            raise TypeError('The argument %s does not meet the minimum length '
                            'requirement of %s.' % (lst, length_min))
        # Check for the maximum length of the list
        if length_max > -1 and len(lst) > length_max:
            raise TypeError('The argument %s does not meet the maximum length '
                            'requirement of %s.' % (lst, length_max))
        return True
