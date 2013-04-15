import numpy
import math
import operator

# Methods common to both the transmitter and receiver.
def hamming(s1,s2):
    # Given two binary vectors s1 and s2 (possibly of different 
    # lengths), first truncate the longer vector (to equalize 
    # the vector lengths) and then find the hamming distance
    # between the two. Also compute the bit error rate  .
    # BER = (# bits in error)/(# total bits )

    # truncate if vectors are of different lengths
    if len(s1) > len(s2):
      s1 = s1[:len(s2)]
    elif len(s2) > len(s1):
      s2 = s2[:len(s1)]

    num_error_bits = 0
    for idx, val in enumerate(s1):
      if val != s2[idx]:
        num_error_bits = num_error_bits + 1

    return num_error_bits, float(num_error_bits)/len(s1)
