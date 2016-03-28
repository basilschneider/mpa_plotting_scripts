#!/usr/bin/env python2

""" Author: Basil Schneider <basil.schneider@cern.ch>
MPA data class to store MPA specific quantitites. """

class MPA(object):

    """ MPA data class to store MPA specific qantitities. The data is stored in
    _no_hits_shutter. This is a list of list with the following structure:
    [[a,b,...], [c,d], ...] - a is the no. of hits on pixel 1 during shutter 1
                              b is the no. of hits on pixel 2 during shutter 1
                              c is the no. of hits on pixel 1 during shutter 2
                              d is the no. of hits on pixel 2 during shutter 2
                              ...
    """

    def __init__(self, no_pxs):

        """ Initialize instances. """

        # Number of pixels
        self.no_pxs = no_pxs

        # Number of hits per shutter
        self._no_hits_shutter = []

    def set_no_hits_shutter(self, no_hits):

        """ Set number of hits per shutter. """

        self.check_if_list(no_hits, self.no_pxs, self.no_pxs)
        self._no_hits_shutter.append(no_hits)

    def get_no_hits_shutter(self):

        """ Get number of hits per shutter. """

        return self._no_hits_shutter

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
