import numpy
import math
import operator
import common_txrx_mil3
import binascii
# Methods common to both the transmitter and receiver

'''
These functions are for modulation and demodulation
(which is currently presented as a black box)
No need to touch them
'''
def modulate (fc, samplerate, samples):
   return common_txrx_mil3.modulate(fc, samplerate, samples)

def demodulate (fc, samplerate, samples):
   return common_txrx_mil3.demodulate(fc, samplerate, samples)

################
'''
If you need any functions that
you need commonly in both transmitter and receiver,
implement here
'''

def get_preamble_bit():
  return numpy.array(
    [1,1,1,1,1,0,1,1,1,1,0,0,1,1,1,0,1,0,1,1,0,0,0,0,1,0,1,1,1,0,0,0,1,1,0,1,1,0,1,0,0,1,0,0,0,1,0,0,1,1,0,0,1,0,1,0,1,0,0,0,0,0,0]
  )
  # return numpy.array(
  #   [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1]
  # )

def convert_bits_to_samples(bits, spb, one):
  '''
  Converts each bits into [spb] samples
  Sample values for bit '1', '0' should be [one], 0 respectively.
  Output should be an array of samples.
  '''
  samples = []
  for bit in numpy.nditer(bits):
      for i in range(spb):
          samples.append(one if bit == 1 else bit)
  return numpy.array(samples)