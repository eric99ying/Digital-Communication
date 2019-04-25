'''
Main script to run for transmitting computer during final demo.
'''

from huffman_encode import *
from error_correction_encode import *
import os

dir_path = os.path.dirname(os.path.abspath(__file__)) + "/"

if __name__ == "__main__":
	huffman_encode.convert("tests/500_char.txt", "encoded/500_char_encode.txt", "frequency_table_2.txt")
	error_correction_encode.berlekamp_welsh_encode(dir_path+"encoded/500_char_encode.txt", 4, dir_path+"error_encoded/500_char_error_encode.txt")
	# transmit sound