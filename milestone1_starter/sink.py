# audiocom library: Source and sink functions
import common_srcsink
import Image
from graphs import *
import binascii
import random
import numpy
import math

class Sink:
    def __init__(self):
        # no initialization required for sink 
        print 'Sink:'

    def process(self, recd_bits):
        # Process the recd_bits to form the original transmitted
        # file. 
        # Here recd_bits is the array of bits that was 
        # passed on from the receiver. You can assume, that this 
        # array starts with the header bits (the preamble has 
        # been detected and removed). However, the length of 
        # this array could be arbitrary. Make sure you truncate 
        # it (based on the payload length as mentioned in 
        # header) before converting into a file.
        
        # If its an image, save it as "rcd-image.png"
        # If its a text, just print out the text
        
        # Return the received payload for comparison purposes
        return rcd_payload

    def bits2text(self, bits):
        # Convert the received payload to text (string)
        return  text

    def image_from_bits(self, bits, filename):
        # Convert the received payload to an image and save it
        # No return value required .
        
        # convert bits to pixel values
        for bit in numpy.nditer(bits, op_flags=['readwrite']):
            if bit[...] != 0:
                bit[...] = 255

        img = Image.new('L', (32,32))
        img.putdata(bits)
        img.save(filename)

    def read_header(self, header_bits): 
        # Given the header bits, compute the payload length
        # and source type (compatible with get_header on source)
 
        print '\tRecd header: ', header_bits

        
        # compute payload length
        payload = header_bits[2:]
        power = len(payload) - 1
        index = 0
        length = 0

        while power >= 0:
            length = length + math.pow(2, power) * payload[index]
            index = index + 1
            power = power - 1

        payload_length = int(length)
        print '\tLength from header: ', payload_length
        
        
        # find source type
        source = header_bits[:2]
        if source[0] is 1 and source[1] is 0:
            srctype = 'image'
        elif source[0] is 0 and source[1] is 1:
            srctype = 'text'
        elif source[0] is 1 and source[1] is 1:
            srctype = 'monotype'
        else:
            srctype = '???'

        print '\tSource type: ', srctype
        return srctype, payload_length