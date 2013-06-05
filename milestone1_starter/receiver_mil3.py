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
  demod_samples = list(demod_samples)
  center1 = min(demod_samples)
  center2 = max(demod_samples)

  have_centers_changed = True
  while have_centers_changed:
    group1 = []
    group2 = []
    for i in range(len(demod_samples)):
      sample = demod_samples[i]
      if (sample-center1)**2 < (sample-center2)**2:
        group1.append(i)
      else:
        group2.append(i)

    new_center1 = 0
    for i in group1:
      new_center1 += demod_samples[i]
    new_center1 /= float(len(group1))

    new_center2 = 0
    for i in group2:
      new_center2 += demod_samples[i]
    new_center2 /= float(len(group2))

    if new_center2 == center2 and new_center1 == center1:
      have_centers_changed = False
    center1 = new_center1
    center2 = new_center2

  # insert code to associate the higher of the two centers
  # with one and the lower with zero
  one = max(center1, center2)
  zero = min(center1, center2)

  print "Threshold for 1:"
  print one
  print " Threshold for 0:"
  print zero

  # insert code to compute thresh
  thresh = (one + zero) / 2
  return one, zero, thresh


