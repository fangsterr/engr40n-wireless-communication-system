import sys
import math
import numpy
import scipy.cluster.vq
import common_txrx as common
from numpy import linalg as LA
import receiver_mil3
import hamming_db

class Receiver:
    def __init__(self, carrier_freq, samplerate, spb):
        '''
        The physical-layer receive function, which processes the
        received samples by detecting the preamble and then
        demodulating the samples from the start of the preamble
        sequence. Returns the sequence of received bits (after
        demapping)
        '''
        self.fc = carrier_freq
        self.samplerate = samplerate
        self.spb = spb

        print 'Receiver: '

    def detect_threshold(self, demod_samples):
        '''
        Calls the detect_threshold function in another module.
        No need to touch this.
        '''
        return receiver_mil3.detect_threshold(demod_samples)

    def detect_preamble(self, demod_samples, thresh, one):
        '''
        Find the sample corresp. to the first reliable bit "1"; this step
        is crucial to a proper and correct synchronization w/ the xmitter.
        '''

        '''
        First, find the first sample index where you detect energy based on the
        moving average method described in the milestone 2 description.
        '''
        could_not_find_energy_offset = True
        energy_offset = 0
        size_of_demod_samples = len(demod_samples)
        while energy_offset < size_of_demod_samples:
            samples = demod_samples[energy_offset:energy_offset + self.spb]
            average_sample_val = self.get_average_central_samples_val(samples)
            if average_sample_val > ((one + thresh) / 2):
                could_not_find_energy_offset = False
                break
            # energy_offset += self.spb
            energy_offset += 1

        if could_not_find_energy_offset:
            print '*** ERROR: Could not detect any ones (so no preamble). ***'
            print '\tIncrease volume / turn on mic?'
            print '\tOr is there some other synchronization bug? ***'
            sys.exit(1)

        '''
        Then, starting from the demod_samples[offset], find the sample index where
        the cross-correlation between the signal samples and the preamble
        samples is the highest.
        '''
        highest_preamble_offset = 0
        highest_correlation = 0
        preamble_samples = common.convert_bits_to_samples(
            common.get_preamble_bit(),
            self.spb,
            one
        )

        size_of_samples_to_analyze = 3 * len(preamble_samples)
        preamble_offset = 0

        while preamble_offset < size_of_samples_to_analyze:
            start = energy_offset
            end = start + len(preamble_samples)
            correlation = self.calc_cross_correlation_val(
                preamble_samples,
                demod_samples[start:end],
            )

            if correlation > highest_correlation:
                highest_correlation = correlation
                highest_preamble_offset = preamble_offset

            preamble_offset += 1

        preamble_offset = highest_preamble_offset

        '''
        [preamble_offset] is the additional amount of offset starting from [offset],
        (not a absolute index reference by [0]).
        Note that the final return value is [offset + pre_offset]
        '''

        return energy_offset + preamble_offset

    def demap_and_check(self, demod_samples, preamble_start):
        '''
        Demap the demod_samples (starting from [preamble_start]) into bits.
        1. Calculate the average values of midpoints of each [spb] samples
           and match it with the known preamble bit values.
        2. Use the average values and bit values of the preamble samples from (1)
           to calculate the new [thresh], [one], [zero]
        3. Demap the average values from (1) with the new three values from (2)
        4. Check whether the first [preamble_length] bits of (3) are equal to
           the preamble. If it is proceed, if not terminate the program.
        Output is the array of data_bits (bits without preamble)
        '''
        preamble_bits = common.get_preamble_bit()

        demod_samples = demod_samples[preamble_start:]
        size_of_samples = len(demod_samples)

        # Get average values of midpoints
        average_midpoint_values_of_samples = []
        index = 0
        while index < size_of_samples:
            samples = demod_samples[index:index + self.spb]
            average_sample_val = self.get_average_central_samples_val(samples)
            average_midpoint_values_of_samples.append(average_sample_val)
            index += self.spb

        # Cal new thres, one, zero using preamble bits
        num_of_one_bits = 0
        num_of_zero_bits = 0
        total_one_val = 0
        total_zero_val = 0
        index = 0
        for bit in preamble_bits:
            if bit == 0:
                total_zero_val += average_midpoint_values_of_samples[index]
                num_of_zero_bits += 1
            else:
                total_one_val += average_midpoint_values_of_samples[index]
                num_of_one_bits += 1
            index += 1

        one = total_one_val / num_of_one_bits
        zero = total_zero_val / num_of_zero_bits
        thresh = (one + zero) / 2

        # Demap
        demapped_bits = []
        for bit_val in average_midpoint_values_of_samples:
            if bit_val > thresh:
                demapped_bits.append(1)
            else:
                demapped_bits.append(0)

        # Check preamble bits (commented out for channel coding)
        # index = 0
        # for bit in preamble_bits:
        #     if not bit == demapped_bits[index]:
        #         print "*** ERROR ***\n"
        #         print "Preamble bits do not match.\n"
        #         sys.exit(1)
        #     index += 1

        # It's all good
        data_bits = numpy.array(demapped_bits[len(preamble_bits):])
        return data_bits

    def demodulate(self, samples):
        return common.demodulate(self.fc, self.samplerate, samples)

    def get_average_central_samples_val(self, samples):
        '''
        Given array of samples, returns the average values of the central values
        '''
        size_of_central_samples = len(samples) / 2
        start = size_of_central_samples / 2
        end = len(samples) - start
        central_samples = samples[start:end]

        total = 0
        for val in central_samples:
            total += val
        avg = total / size_of_central_samples

        return avg

    def calc_cross_correlation_val(self, preamble_samples, samples):
        '''
        Return the cross correlation value between preamble samples and current
        samples analyzed
        '''
        return (numpy.dot(preamble_samples, samples) / numpy.linalg.norm(samples))

    def decode(self, rcd_bits):
        return rcd_bits

        header = rcd_bits[:16*3]
        decoded_header = self.hamming_decoding(header, 0)
        header_coding_rate = decoded_header[:5]

        bit_string = ""
        for bit in header_coding_rate:
            single_bit_string = '%d' % bit
            bit_string += single_bit_string
        header_coding_rate = int(bit_string, 2)

        bit_string = ""
        header_coded_frame_length = decoded_header[5:16]
        for bit in header_coded_frame_length:
            single_bit_string = '%d' % bit
            bit_string += single_bit_string
        header_coded_frame_length = int(bit_string, 2)

        print "channel coding rate: %d" % header_coding_rate
        import pdb; pdb.set_trace()
        decoded_bits = self.hamming_decoding(
            rcd_bits[16*3:header_coded_frame_length],
            header_coding_rate
        )
        import pdb; pdb.set_trace()
        return decoded_bits

    def hamming_decoding(self, coded_bits, index):
        n, k, H = hamming_db.parity_lookup(index)

        split_up_blocks = numpy.reshape(coded_bits, (-1, n))

        decoded_bits = []
        error_count = 0

        reshaped_H = numpy.reshape(H,H.size,order='F').reshape((n,H.size/n))
        import pdb; pdb.set_trace()
        for block in split_up_blocks:
            original_bits = block[:k]
            syndrome = numpy.dot(H, block)

            for index in range(len(syndrome)):
                if syndrome[index] % 2 == 0:
                    syndrome[index] = 0
                else:
                    syndrome[index] = 1

            for element in syndrome:
                if element != 0:
                    error_count += 1

                    second_count = 0
                    for column in reshaped_H:
                        if second_count >= k:
                            break
                        if numpy.array_equal(column, syndrome):
                            if block[second_count] == 0:
                                block[second_count] = 1
                            else:
                                block[second_count] = 0
                            break
                        second_count += 1
                    original_bits = block[:k]
                    break

            decoded_bits = numpy.append(decoded_bits, original_bits)

        print "errors corrected: %d" % error_count
        return numpy.array(decoded_bits)
