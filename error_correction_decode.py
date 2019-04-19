'''
error_correction_decode.py
~~~
Perform berlekamp-welsh to decode the encoded transmitted bits. Writes to an output file. 

message-> huffman_encode -> error_correction_encode -> transmission -> receive 
-> error_correction_decode -> huffman_decode -> retrieved message
'''
import os
import re
from berlekamp_welsh import welchberlekamp as wb
from berlekamp_welsh.finitefield.finitefield import FiniteField


NUM_SOUNDS = 16
N = 16
K = 12
P = 17

fp = FiniteField(P)

dir_path = os.path.dirname(os.path.abspath(__file__)) + "/"


def read_message(input_file):
	'''
	Takes in an input file and converts the integers in the file to points on polynomials.

	Args:
		input_file (str): The input file name.
	Return:
		list: A list of the points on polynomials. ie. [[0, 3], [1, 2], [2, 15],...]
	'''
	packets = []
	cur_n = 0
	with open(input_file, "r") as in_file:
		b = in_file.readline()
		while b:
			b = int(re.match("\d+", b).group())
			packets.append([fp(cur_n), fp(b)])  # Append the x and y points of the polynomial
			cur_n = (cur_n + 1)%N
			b = in_file.readline()
	return packets


def decode(points, n, k, p, output_file, m):
	'''
	Decodes the points and tries to reconstruct original polynomial. Writes the binary bits to 
	output_file.

	Args:
		points (list): The list of points from read_message.
		n (int): The number of packets transmitted for each k values. n > k for redundancy.
		k (int): The degree of the polynomial that we want to figure out.
		p (int): Modulo space. p > n > k
		output_file (str): The name of the output text file.
		m (int): The number of bits grouped together. Usually we would group 4 bits together.
	Returns:
		list: The coefficients of the polynomials decoded.
	'''
	encoder, decoder, s = wb.makeEncoderDecoder(n, k, p)
	decoded_message = []
	i = 0
	final_message = ""
	while i < len(points):
		#print(points[i:i+n])
		dm = list(decoder(points[i:i+n]))
		if len(dm) < k:
			dm.append(0)
		decoded_message.extend(dm)
		i = i+n
		for j in dm: 
			final_message += str(bin(int(j))[2:].zfill(m))[-m:]

	with open(output_file, "w") as out_file:
		out_file.write(final_message)

	return decoded_message

def berlekamp_welsh_decode(input_file, m, output_file):
	packets = read_message(input_file)
	decode(packets, N, K, P, output_file, m)
	print("Error Decoding successful.")
	print("__________________________")


if __name__ == "__main__":
	berlekamp_welsh_decode(dir_path+"error_encoded/500_char_error_encode.txt", 4, dir_path+"error_decoded/500_char_error_decode.txt")


