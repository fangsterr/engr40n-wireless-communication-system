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