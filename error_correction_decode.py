'''
error_correction_decode.py
~~~
Perform berlekamp-welsh to decode the encoded transmitted bits.
'''
import os
from berlekamp-welsh import welshberlekamp as wb

num_sounds = 16
n = 16
k = 12
p = 17

dir_path = os.path.dirname(os.path.abspath(__file__)) + "/"


def receive_message(input_file):
	bits = []
	cur_n = 0
	with open(dir_path + input_file, "r") as in_file:
		b = in_file.read(1)
		while b:
			bits.append((cur_n, b))
			cur_n = (cur_n + 1)%n
			b = in_file.read(1)
	return bits


def decode(decoded_points, n, k, p):
	encoder, decoder, s = wb.makeEncoderDecoder(n, k, p)
	decoded_message = []
	i = 0
	while i < len(decoded_points)
		decoded_message.extend(list(decoder(decoded_points[i:i+n])))
		i = i+n
	return deocded_message
