import numpy
import math
import operator
import random
import scipy.cluster.vq
import common_txrx as common

def detect_threshold(demod_samples):
        # Now, we have a bunch of values that, for on-off keying, are
        # either near amplitude 0 or near a positive amplitude
        # (corresp. to bit "1").  Because we don't know the balance of
        # zeroes and ones in the input, we use 2-means clustering to
        # determine the "1" and "0" clusters.  In practice, some
        # systems use a random scrambler to XOR the input to balance
        # the zeroes and ones. We have decided to avoid that degree of
        # complexity in audiocom (for the time being, anyway).

	# initialization
  center1 = min(demod_samples)
  center2 = max(demod_samples)

  # insert code to implement 2-means clustering

  # insert code to associate the higher of the two centers
  # with one and the lower with zero

  one = 1
  zero = 0

  print "Threshold for 1:"
  print one
  print " Threshold for 0:"
  print zero

  # insert code to compute thresh
  thresh = (one + zero) / 2
  return one, zero, thresh


