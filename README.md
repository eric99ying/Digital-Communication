# Digital-Communication
EE126 Project
Eric, Amal, Srikar, Wesley

This project attempts to communicate a text file from one computer to another using only speakers and microphones.

Pipeline:

message-> huffman_encode -> error_correction_encode -> transmission -> receive-> error_correction_decode -> huffman_decode -> retrieved message



Source:

Berlekamp-Welsh library: https://github.com/j2kun/welch-berlekamp
