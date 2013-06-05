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
    modulated_sample = sample * math.cos(2 * math.pi * ((fc * 1.0) / samplerate) * index)
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
    demodulated_sample = sample * cmath.exp((2j * math.pi * fc * index) / (samplerate * 1.0))
    demodulated_samples.append(demodulated_sample)
    index = index + 1

  omega_cut = 2 * math.pi * (fc / (2.0 * samplerate))

  return lpfilter(demodulated_samples, omega_cut)

def lpfilter(samples_in, omega_cut):
  '''
  A low-pass filter of frequency omega_cut.
  '''
  # set the filter unit sample response
  L = 50

  unit_sample_response_array = []
  index = L * (-1)
  while index <= L:
    if index == 0:
      unit_sample_response = omega_cut / math.pi
    else:
      unit_sample_response = math.sin(omega_cut * index) / (math.pi * index * 1.0)
    unit_sample_response_array.append(unit_sample_response)
    index = index + 1
  unit_sample_response_array = numpy.array(unit_sample_response_array)

  # compute the demodulated samples
  demod_samples = []
  index = 0
  for sample in samples_in:
    samples_subarray = numpy.zeros(len(unit_sample_response_array), dtype=numpy.dtype(complex))
    samples_in_len = len(samples_in)
    second_index = index + L
    array_index = 0
    while second_index >= index - L:
      if not (second_index < 0 or second_index >= samples_in_len):
        samples_subarray[array_index] = samples_in[second_index]
      array_index = array_index + 1
      second_index = second_index - 1

    value = numpy.dot(samples_subarray, unit_sample_response_array)
    demod_samples.append(abs(value))
    index = index + 1

  return demod_samples
