Source encoding --
In source.py, we populate a frequency map for all the different 4-bit sequences found in the source bits. Then, we create a Huffman encoding tree from the frequency map, breaking ties by examining the symbols. After that, we create a code map that maps a symbol to its code in the Huffman tree. We use this code map to encode the source bits. We store the header as specified in the assignment outline.

In sink.py, we re-create the frequency map from the header and reconstruct the Huffman encoding tree from the encoding map. Then, we use the Huffman tree to decode the encoded bits back into the source bits.

Channel coding --

In hamming_db.py, we implemented the functions that creates the generator and parity matrices for the associated indexes. These were then used to encode and decode the bits, in transmitter.py and receiver.py, respectively. 

Modulation/demodulation --

In common_txrx_mil3.py, we implemented the modulate and demodulate functions. The demodulated samples were passed through a low pass filter.

In receiver_mil3.py, we calculate the thresholds for 0 and 1 using the 2-means algorithm detailed in the assignment handout.