'''
Main script to run for transmitting computer during final demo.
'''

from huffman_encode import *
from error_correction_encode import *
import os
from text_to_sound import *
from test import *
import parameters

dir_path = os.path.dirname(os.path.abspath(__file__)) + "/"

if __name__ == "__main__":
	convert(parameters.input_text_file, parameters.huffman_encode_output, "frequency_table_2.txt")
	berlekamp_welsh_encode(dir_path+parameters.huffman_encode_output, parameters.group, dir_path+parameters.error_encode_output)
	
	# Play sound
	construct_wav(parameters.error_encode_output, 1500, 7000, 131, make_wav_obj())
	play_wav()
