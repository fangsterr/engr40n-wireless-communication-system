import math
import common_txrx as common
import numpy

class Transmitter:
    def __init__(self, carrier_freq, samplerate, one, spb, silence, cc_len):
        self.fc = carrier_freq  # in cycles per sec, i.e., Hz
        self.samplerate = samplerate
        self.one = one
        self.spb = spb
        self.silence = silence
        self.cc_len = cc_len
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
        preamble = common.get_preamble_bit()
        return numpy.concatenate((silence_bits, preamble, databits))


    def bits_to_samples(self, databits_with_preamble):
        '''
        Convert each bits into [spb] samples.
        Sample values for bit '1', '0' should be [one], 0 respectively.
        Output should be an array of samples.
        '''
        return common.convert_bits_to_samples(
            databits_with_preamble,
            self.spb,
            self.one
        )


    def modulate(self, samples):
        '''
        Calls modulation function. No need to touch it.
        '''
        return common.modulate(self.fc, self.samplerate, samples)


    def encode(self, databits):
        index, coded_data = hamming_encoding(databits)

        header_coding_rate = numpy.binary_repr(index, width=5)
        header_coded_frame_length = numpy.binary_repr(len(coded_data) + 16, width=11)
        coded_header = header_coding_rate + header_coded_frame_length
        index, coded_header = hamming_encoding(coded_header, True)

        return numpy.append(coded_header, coded_data)

    def hamming_encoding(self, databits, is_header):
        cc_len = self.cc_len
        if is_header:
            cc_len = 3

        n, k, index, G = gen_lookup(cc_len)

        offset = len(databits) % k
        for bit in range(offset):
            databits.append(0)

        coded_bits = []

        # break into k sized blocks
        k_block_bit = []
        count = 0
        for bit in numpy.nditer(databits):
            k_block_bit.append(bit)
            if (count % k) == (k-1):
                bits = numpy.dot(k_block_bit, G)
                coded_bits.append(bits)
            count += 1

        coded_bits = numpy.array(coded_bits)
        return index, coded_bits
