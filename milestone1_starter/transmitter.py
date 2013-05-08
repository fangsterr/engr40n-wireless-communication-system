import math
import common_txrx as common
import numpy

class Transmitter:
    def __init__(self, carrier_freq, samplerate, one, spb, silence):
        self.fc = carrier_freq  # in cycles per sec, i.e., Hz
        self.samplerate = samplerate
        self.one = one
        self.spb = spb
        self.silence = silence
        print 'Transmitter: '

    def add_preamble(self, databits):
        '''
        Prepend the array of source bits with silence bits and preamble bits
        The recommended preamble bits is 
        [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1]
        The output should be the concatenation of arrays of
            [silence bits], [preamble bits], and [databits]
        '''
        silence_bits = []
        for i in range(self.silence):
            silence_bits.append(0)

        silence_bits = numpy.array(silence_bits)
        preamble = numpy.array([1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1])
        return numpy.append(silence_bits, preamble, databits)


    def bits_to_samples(self, databits_with_preamble):
        '''
        Convert each bits into [spb] samples. 
        Sample values for bit '1', '0' should be [one], 0 respectively.
        Output should be an array of samples.
        '''
        samples = []
        for bit in numpy.nditer(databits_with_preamble):
            for i in range(self.spb):
                samples.append(self.one if bit == 1 else bit)
        return return numpy.array(samples)
        

    def modulate(self, samples):
        '''
        Calls modulation function. No need to touch it.
        '''
        return common.modulate(self.fc, self.samplerate, samples)
