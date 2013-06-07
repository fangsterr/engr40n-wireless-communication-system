import numpy
import math
import operator
import common_txrx_mil3
import binascii
import sys

generating_matrices = [numpy.array([1, 1, 1]),
                       numpy.array([1,    1,    0,    1,    0,    0,    0,
                                    0,    1,    1,    0,    1,    0,    0,
                                    1,    1,    1,    0,    0,    1,    0,
                                    1,    0,    1,    0,    0,    0,    1]),
                       numpy.array([1,     1,     0,     0,     1,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
                                    0,     1,     1,     0,     0,     1,     0,     0,     0,     0,     0,     0,     0,     0,     0,
                                    0,     0,     1,     1,     0,     0,     1,     0,     0,     0,     0,     0,     0,     0,     0,
                                    1,     1,     0,     1,     0,     0,     0,     1,     0,     0,     0,     0,     0,     0,     0,
                                    1,     0,     1,     0,     0,     0,     0,     0,     1,     0,     0,     0,     0,     0,     0,
                                    0,     1,     0,     1,     0,     0,     0,     0,     0,     1,     0,     0,     0,     0,     0,
                                    1,     1,     1,     0,     0,     0,     0,     0,     0,     0,     1,     0,     0,     0,     0,
                                    0,     1,     1,     1,     0,     0,     0,     0,     0,     0,     0,     1,     0,     0,     0,
                                    1,     1,     1,     1,     0,     0,     0,     0,     0,     0,     0,     0,     1,     0,     0,
                                    1,     0,     1,     1,     0,     0,     0,     0,     0,     0,     0,     0,     0,     1,     0,
                                    1,     0,     0,     1,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     1]),
                       numpy.array([ 1,    0,     1,     0,     0,     1,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
                                     0,    1,    0,    1,     0,     0,     1,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
                                     0,    0,    1,    0,     1,     0,     0,     1,     0,     0,     0,     0,     0,     0,     0,     0,     0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    0,    1,    1,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     0,    1,    0,    1,    1,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    0,    0,    0,    1,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     0,    1,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     0,    0,    1,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    0,    1,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    1,    1,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    1,    0,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    1,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     0,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     0,    0,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     0,    0,    0,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    0,    1,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    1,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,
                                     0,    1,    1,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,
                                     1,    0,    0,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,
                                     1,    1,    1,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,
                                     1,    1,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,
                                     0,    1,    1,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,
                                     1,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,
                                     0,    1,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1])]

parameters = [[3,1],[7,4],[15,11],[31,26]]


def gen_lookup(cc_len):
    '''
    returns
    (1) n (=cc_len, codeword length)
    (2) k (length of data bit in each codeword)
    (3) index (index of the corresponding code in the above lookup table)
    (4) generater matrix
    for Hamming code with n = cc_len
    '''
    if cc_len == 3:
        index = 0
    elif cc_len == 7:
        index = 1
    elif cc_len == 15:
        index = 2
    elif cc_len == 31:
        index = 3
    else:
        print '\tNo Hamming code with n =', cc_len
        sys.exit(1)

    n = parameters[index][0]
    k = parameters[index][1]

    # Reshape G:
    old_G = generating_matrices[index]
    old_G = numpy.reshape(old_G, (k, n))
    A, identity = numpy.hsplit(old_G, [n-k])
    G = numpy.concatenate((identity, A), 1)
    # G = numpy.reshape(G,G.size,order='F').reshape((n,k))

    return n, k, index, G

def parity_lookup(index):
    '''
    returns the
    (1) n (=cc_len, codeword length)
    (2) k (length of data bit in each codeword)
    (3) index (index of the corresponding code in the above lookup table)
    (4) parity check matrix
    matched by the lookup table above given the index
    The reason why this takes the index as the input while gen_lookup takes cc_len
    is, because containing index is efficient than containing n in the header.
    The decoder reads the header to pick the right parity check matrix.
    '''
    G = generating_matrices[index]
    n = parameters[index][0]
    k = parameters[index][1]

    # Reshape G, extract A and compute H:
    G = numpy.reshape(G, (k, n))
    A, identity = numpy.hsplit(G, [n-k])
    A_checker = numpy.transpose(A)
    identity_checker = numpy.identity(n-k, dtype=int)
    H = numpy.concatenate((A_checker, identity_checker), 1)
    # H = numpy.reshape(H,H.size,order='F').reshape((n,H.size/n))

    return n, k, H



