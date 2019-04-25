'''
receive_main.py
~~~
Main script that receiving computer runs during final demo.
'''


from huffman_decode import *
from error_correction_decode import *
import os

dir_path = os.path.dirname(os.path.abspath(__file__)) + "/"

if __name__ == "__main__":
	error_correction_decode.berlekamp_welsh_decode(dir_path+"classify.txt", 4, dir_path+"error_decoded/error_decoded_500_char.txt")
	huffman_decode.devert("error_decoded/error_decoded_500_char.txt", "decoded/500_char_decode_FINAL.txt", "frequency_table_2.txt")
	# transmit sound