'''
receive_main.py
~~~
Main script that receiving computer runs during final demo.
'''


from huffman_decode import *
from error_correction_decode import *
import real_time_fft as fft
import os
import parameters

dir_path = os.path.dirname(os.path.abspath(__file__)) + "/"

if __name__ == "__main__":
	# Receive sound
	fft.main()
	berlekamp_welsh_decode(dir_path+parameters.receive_output, parameters.group, dir_path+parameters.error_decode_output)
	devert(parameters.error_decode_output, parameters.huffman_decode_output, "frequency_table_2.txt")
