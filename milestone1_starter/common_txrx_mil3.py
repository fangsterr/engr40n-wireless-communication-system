import numpy
import math
import operator
import cmath

# Methods common to both the transmitter and receiver
def modulate(fc, samplerate, samples):
  '''
  A modulator that multiplies samples with a local carrier
  of frequency fc, sampled at samplerate
  '''
  modulated_samples = []
  index = 0
  for sample in samples:
    modulated_sample = math.cos(2 * math.pi * ((fc * 1.0) / samplerate) * index)
    modulated_samples.append(modulated_sample)
    index = index + 1

  return modulated_samples

def demodulate(fc, samplerate, samples):
  '''
  A demodulator that performs quadrature demodulation
  '''
  demodulated_samples = []
  index = 0
  for sample in samples:
    demodulated_sample = mod(fc, samplerate, index)
    demodulated_samples.append(demodulated_sample)
    index = index + 1

  omega_cut = 2 * math.pi * (fc / (2.0 * samplerate))

  return lpfilter(demodulated_samples, omega_cut, fc, samplerate)

def lpfilter(samples_in, omega_cut, fc, fs):
  '''
  A low-pass filter of frequency omega_cut.
  '''
  # set the filter unit sample response
  L = 50

  # compute the demodulated samples
  # This is probably wrong...
  demod_samples = []
  index = 0
  for sample in samples_in:
    if index == 0:
      unit_sample_response = omega_cut / math.pi
    elif (-1 * L) <= index <= L:
      unit_sample_response = math.sin(omega_cut * index) / (math.pi * index * 1.0)
    else:
      unit_sample_response = 0

    demod_sample = abs(sample * mod(fc, fs, index) * unit_sample_response)
    demod_samples.append(demod_sample)
    index = index + 1

  print demod_samples
  return demod_samples


def mod(fc, fs, n):
  return cmath.exp(2j * math.pi * fc * n / (fs * 1.0))

