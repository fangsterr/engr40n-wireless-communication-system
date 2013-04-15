# audiocom library: Source and sink functions
import common_srcsink as common
import Image
from graphs import *
import binascii
import random



class Source:
    def __init__(self, monotone, filename=None):
        # The initialization procedure of source object
        self.monotone = monotone
        self.fname = filename
        print 'Source: '

    def process(self):
            # Form the databits, from the filename
            if self.fname is not None:
                if self.fname.endswith('.png') or self.fname.endswith('.PNG'):
                    # Its an image
                else:
                    payload = text2bits(self, self.fname)
                    databits = get_header(self, len(payload), 'text') + payload
            else:
                # Send monotone (the payload is all 1s for
                # monotone bits)
            return payload, databits

    def text2bits(self, filename):
        # Given a text file, convert to bits

        # Read file
        f = open(filename)
        data = f.read()
        f.close()

        # Convert each char to bit
        bits = numpy.array([])
        for char in data:
            ascii = ord(char)
            bit_string = '{0:08b}'.format(ascii)
            for bit in bit_string:
                if bit is '0':
                    bits = numpy.append(bits, [0])
                else:
                    bits = numpy.append(bits, [1])

        return bits

    def bits_from_image(self, filename):
        # Given an image, convert to bits
        return bits

    def get_header(self, payload_length, srctype):
        # Given the payload length and the type of source
        # (image, text, monotone), form the header
        return header
