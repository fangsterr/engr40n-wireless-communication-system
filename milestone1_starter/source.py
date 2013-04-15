# audiocom library: Source and sink functions
import common_srcsink as common
import Image
from graphs import *
import binascii
import numpy
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
                    payload = self.bits_from_image(self.fname)
                    databits = numpy.append(
                        self.get_header(len(payload), 'image'),
                        payload
                    )
                else:
                    payload = self.text2bits(self.fname)
                    databits = numpy.append(
                        self.get_header(len(payload), 'text'),
                        payload
                    )
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
        img = Image.open(filename)
        img = img.convert('L')
        bits = numpy.array(list(img.getdata()))  # read in as pixels, need to
                                                 # convert to bits
        for num in numpy.nditer(bits, op_flags=['readwrite']):
            if num[...] != 0:
                num[...] = 1

        return bits

    def get_header(self, payload_length, srctype):
        # Given the payload length and the type of source
        # (image, text, monotone), form the header

        if srctype is 'image':
            header_type = [1, 0]
            header_length = []
            header_length_str = numpy.binary_repr(payload_length, width=6)
            for bit in header_length_str:
                header_length.append(int(bit))
            header = header_type + header_length

        return numpy.array(header)
