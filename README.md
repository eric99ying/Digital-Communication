# Digital-Communication
EE126 Project
Eric, Amal, Srikar, Wesley

This project attempts to communicate a text file from one computer to another using only speakers and microphones.

Pipeline:

message-> huffman_encode -> error_correction_encode -> transmission -> receive-> error_correction_decode -> huffman_decode -> retrieved message

To run this code, modify parameters.py such that the path to the text file to be transferred is in the variable input_text_file.
Then, the laptop with the text file runs transmit_main.py and the other laptop runs receive_main.py.
It is recommended to run receive_main.py first to ensure that the laptop is ready and waiting for sounds before the other laptop starts transmitting.


Source:

Berlekamp-Welsh library: https://github.com/j2kun/welch-berlekamp
