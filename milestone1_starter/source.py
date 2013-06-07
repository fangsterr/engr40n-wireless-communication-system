# audiocom library: Source and sink functions
import common_srcsink as common
import Image
from graphs import *
import binascii
import numpy
import random
from Queue import PriorityQueue
import collections

class ENode:
    def __init__(self):
        self.one = None
        self.zero = None
        self.value = None
        self.symbol = None  # only if leaf node
        print "ENode"

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
            payload = numpy.array([1,1,1,1,1,1])
            databits = numpy.append(
                self.get_header(len(payload), 'monotone'),
                payload
            )

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

        bits = bits.astype(int)

        return bits


    def bits_from_image(self, filename):
        img = Image.open(filename)
        img = img.convert('L')
        data = numpy.array(list(img.getdata()))  # read in as pixels, need to
                                                 # convert to bits

        bits = numpy.array([])
        for pixel in data:
            bit_string = numpy.binary_repr(pixel, width=8)
            for bit in bit_string:
                if bit is '0':
                    bits = numpy.append(bits, [0])
                else:
                    bits = numpy.append(bits, [1])

        bits = bits.astype(int)

        return bits


    def populate_code_map(self, node, code_map, prefix=""):
        if node is None:
            return

        if node.symbol is not None:
            code_map[node.symbol] = prefix
            return

        populate_code_map(self, node.zero, code_map, prefix+"0")
        populate_code_map(self, node.one, code_map, prefix+"1")


    def huffman_encode(self, src_bits):
        frequency_map = collections.defaultdict(lambda: 0)
        src_bits = list(src_bits)

        current_symbol = ""
        for i in range(len(src_bits)):
            current_symbol += str(src_bits[i])
            if len(current_symbol) == 4:
                frequency_map[current_symbol] += 1
                current_symbol = ""

        q = PriorityQueue()
        for symbol, freq in frequency_map.iteritems():
            node = ENode()
            node.value = freq * 1000000 + int(symbol)
            node.symbol = symbol
            q.put(node, freq)

        # TODO deal with ties
        while q.qsize() > 1:
            node0 = q.get()
            node1 = q.get()

            merged = ENode()
            merged.value = node1.value + node0.value
            merged.one = node1
            merged.zero = node0

            q.put(merged, merged.value)

        huffman_tree = q.get()

        code_map = {}
        populate_code_map(self, huffman_tree, code_map)

        huffman_encoded_bits = []
        current_symbol = ""
        for i in range(len(src_bits)):
            current_symbol += str(src_bits[i])
            if len(current_symbol) == 4:
                code = code_map[current_symbol]
                for bit in code:
                    huffman_encoded_bits.append(int(bit))
                current_symbol = ""
        huffman_encoded_bits = numpy.array(huffman_encoded_bits)
        return (frequency_map, huffman_encoded_bits)





    def get_header(self, data_length, srctype, data_statistics=None):
        # Given the payload length and the type of source
        # (image, text, monotone), form the header

        # Add source
        if srctype is 'image':
            header_type = [1, 0]
        elif srctype is 'text':
            header_type = [0, 1]
        else:
            header_type = [1, 1]

        # Add length
        header_length = []
        header_length_str = numpy.binary_repr(data_length, width=16)
        for bit in header_length_str:
            header_length.append(int(bit))
        header = header_type + header_length

        if srctype is 'image' or srctype is 'text':
            # huffman dat shiet
            i = 0
            while i <= 1111:
                symbol = str(i)
                while len(symbol) < 4:
                    symbol = "0" + symbol
                freq_str = numpy.binary_repr(data_statistics[symbol], width=10)
                freq_arr = []
                for bit in freq_str:
                    freq_arr.append(int(bit))

                header = header + freq_arr
                i += 1

        return numpy.array(header)
