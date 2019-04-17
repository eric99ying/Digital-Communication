'''
error_correction_decode.py
~~~
Perform berlekamp-welsh to decode the encoded transmitted bits.
'''
import os
import re
from berlekamp_welsh import welchberlekamp as wb
from berlekamp_welsh.finitefield.finitefield import FiniteField


NUM_SOUNDS = 16
N = 16
K = 12
P = 97

fp = FiniteField(P)

dir_path = os.path.dirname(os.path.abspath(__file__)) + "/"


def read_message(input_file):
	'''
	Takes in an input file and converts the integers in the file to points on polynomials.

	Args:
		input_file (str): The input file name.
	Return:
		list: A list of the points on polynomials. 
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
		points
	'''
	encoder, decoder, s = wb.makeEncoderDecoder(n, k, p)
	decoded_message = []
	i = 0
	while i < len(points):
		#print(points[i:i+n])
		decoded_message.extend(list(decoder(points[i:i+n])))
		i = i+n

	final_message = ""
	for j in decoded_message:
		final_message += bin(int(j))[2:].zfill(m)

	with open(output_file, "w") as out_file:
		out_file.write(final_message)

	return decoded_message

def berlekamp_welsh_decode(input_file, m, output_file):
	packets = read_message(input_file)
	decode(packets, N, K, P, output_file, m)
	print("Error Decoding successful.")
	print("__________________________")


if __name__ == "__main__":
	berlekamp_welsh_decode(dir_path+"error_encoded/ErrorEncodeFile4.txt", 4, dir_path+"error_decoded/ErrorDecodeFile4.txt")


