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
                    # Its an image
                else:           
                    # Assume it's text                    
            else:               
                # Send monotone (the payload is all 1s for 
                # monotone bits)   
            return payload, databits

    def text2bits(self, filename):
        # Given a text file, convert to bits
        return bits

    def bits_from_image(self, filename):
        img = Image.open(filename)
        img = img.convert('L')
        bits = list(img.getdata())  # read in as pixels, need to convert to 0/1
        for num in numpy.nditer(bits, op_flags=['readwrite']):
            if num[...] != 0:
                num[...] = 1

        return bits

    def get_header(self, payload_length, srctype): 
        # Given the payload length and the type of source 
        # (image, text, monotone), form the header
        return header
