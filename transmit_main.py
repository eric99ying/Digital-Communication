'''
Main script to run for transmitting computer during final demo.
'''

from huffman_encode import *
from error_correction_encode import *
import os
from text_to_sound import *
from test import *

dir_path = os.path.dirname(os.path.abspath(__file__)) + "/"

if __name__ == "__main__":
	convert("tests/500_char.txt", "encoded/500_char_encode.txt", "frequency_table_2.txt")
	berlekamp_welsh_encode(dir_path+"encoded/500_char_encode.txt", 7, dir_path+"error_encoded/500_char_error_encode.txt")
	construct_wav("error_encoded/500_char_error_encode.txt", 1500, 7000, 131, make_wav_obj())
	play_wav()

	# transmit sound