# audiocom library: Source and sink functions
import common_srcsink
import Image
from graphs import *
import binascii
import random
import numpy
import math
from Queue import PriorityQueue

class DNode:
    def __init__(self):
        self.one = None
        self.zero = None
        self.value = None
        self.symbol = None  # only if leaf node


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

        srctype, payload_length = self.read_type_size(recd_bits[:18])
        rcd_payload = recd_bits[18:]
        rcd_header = rcd_payload[:160]
        rcd_payload = rcd_payload[160:160+payload_length]
        # print 'encoded_bits: ', list(rcd_payload)
        if srctype is 'text':
            freq_map = self.read_stat(rcd_header)
            rcd_payload = self.huffman_decode(freq_map, rcd_payload)
            # print 'payload: ', list(rcd_payload)
            # print 'len(payload): ', len(rcd_payload)
            # print self.bits2text(rcd_payload)
        elif srctype is 'image':
            freq_map = self.read_stat(rcd_header)
            rcd_payload = self.huffman_decode(freq_map, rcd_payload)
            self.image_from_bits(rcd_payload, 'rcd-image.png')

        return rcd_payload

    def bits2text(self, bits):
        # Convert the received payload to text (string)
        text = ""
        index = 0
        bit_string = ""
        for bit in numpy.nditer(bits):
            single_bit_string = '%d' % bit
            bit_string += single_bit_string
            if index % 8 == 7:
                ascii = int(bit_string, 2)
                text += chr(ascii)
                bit_string = ""
            index += 1

        return text

    def image_from_bits(self, bits, filename):
        # Convert the received payload to an image and save it
        # No return value required .
        bitmap = []
        index = 0
        bit_string = ""
        for bit in numpy.nditer(bits):
            single_bit_string = '%d' % bit
            bit_string += single_bit_string
            if index % 8 == 7:
                pixel = int(bit_string, 2)
                bitmap.append(pixel)
                bit_string = ""
            index += 1

        img = Image.new('L', (32,32))
        img.putdata(bitmap)
        img.save(filename)


    def huffman_decode(self, stat, encoded_bits):
        freq_map = stat
        q = PriorityQueue()
        for symbol, freq in freq_map.iteritems():
            node = DNode()
            node.value = (freq * 1000000 + int(symbol))
            node.symbol = symbol
            q.put((node.value, node))

        while q.qsize() > 1:
            value, node0 = q.get()
            value, node1 = q.get()

            merged = DNode()
            merged.value = node0.value + node1.value
            merged.zero = node0
            merged.one = node1

            q.put((merged.value, merged))

        value, huffman_tree = q.get()

        source_bits = []

        node = huffman_tree
        curr_str = ""
        i = 0
        while i < len(encoded_bits):
            bit = encoded_bits[i]
            next_node = node.zero if bit == 0 else node.one

            if next_node is None:
                if node.symbol is None:
                    print 'wtf corrupt huffman tree'
                else:
                    for bitt in node.symbol:
                        source_bits.append(int(bitt))
                node = huffman_tree
                curr_str = ""
                i -= 1
            else:
                node = next_node
                curr_str += "0" if bit == 0 else "1"
            i += 1
        return numpy.array(source_bits)

    def read_stat(self, header_bits):
        frequency_map = {}
        counter = 0
        bit_string = ""
        symbol = 0
        for bit in header_bits:
            counter += 1
            bit_string += str(bit)
            if counter == 10:
                freq = int(bit_string, 2)
                symbol_as_str = numpy.binary_repr(symbol, width=4)
                frequency_map[symbol_as_str] = freq
                symbol += 1
                counter = 0
                bit_string = ""

        return frequency_map



    def read_type_size(self, header_bits):
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
        if source[0] == 1 and source[1] == 0:
            srctype = 'image'
        elif source[0] == 0 and source[1] == 1:
            srctype = 'text'
        elif source[0] == 1 and source[1] == 1:
            srctype = 'monotype'
        else:
            srctype = '???'

        print '\tSource type: ', srctype
        return srctype, payload_length