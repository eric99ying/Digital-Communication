'''
error_correction.py
~~~
Corrects errors in tranmission of bits through Reed Soloman and Berlekemp-Welsh. This file takes in 
the huffman encoded binary file. It groups the bits in the binary file together, then treats each "packet" 
as a coefficient of polynomial. We encode ever K packets into a polynomial, and transmit N points over. P is
the modulo space we work in, and thus must be larger than N or K. 

Pipeline

huffman_encode -> error_correction_encode -> transmission -> receive -> error_correction_decode -> huffman_decode
'''

from berlekamp_welsh import welchberlekamp as wb
import os
import random

dir_path = os.path.dirname(os.path.abspath(__file__)) + "/"

#number of unique sounds
#p corresponds to the closest prime number greater than num_sounds
NUM_SOUNDS = 16
N = 16
K = 12
P = 17

def split_message(input_file, m):
	'''
	Takes in an input file consisting of binary bits and splits it into groups of m bits.

	Args:
		input_file (str): The name of input file.
		m (int): The number of bits to split by.
	Return:
		list: The grouped bits in a list.
	'''
	packets = []
	track = 0
	num_bits_sofar = 0
	num_packets_sofar = 0
	with open(input_file, "r") as in_file:
		b = in_file.read(1)
		while b:
			track = track*2 + int(b)
			num_bits_sofar += 1
			if num_bits_sofar >= m:
				packets.append(track)
				num_bits_sofar = 0
				num_packets_sofar = (num_packets_sofar + 1)
				track = 0
			b = in_file.read(1)
		# Ensure that each packet in "packets" is exactly m bits long
		if num_bits_sofar != 0:
			while num_bits_sofar < m:
				track = track*2
				num_bits_sofar += 1
			packets.append(track)
			num_packets_sofar += 1
		# Ensures there are a multiple of K packets
		if num_packets_sofar != 0:
			#print("initial: ", num_packets_sofar)
			while num_packets_sofar%K != 0:
				packets.append(0)
				num_packets_sofar += 1
				#print(num_packets_sofar)

	print("num packets: ", len(packets))
	return packets


def encode(packets, n, k, p, output_file):
	'''
	Takes list of grouped bits and encode using B-W algorithm. Writes to an output file.
	
	Args:
		bits(list): The list of bits.
		n: The number of packets sent
		k: The actual degree of the polynomial you want to encode
		p: Modulo
			k < n < p
		output_file (str): The file to write the encoded points to.
	Returns:

	'''
	encoder, decoder, _ = wb.makeEncoderDecoder(n, k, p)
	bw_encoded_points = []
	bw_written_points = ""
	i = 0
	while i < len(packets):
		chunk = [packets[j] for j in range(i, i+k)]
		i += k
		points = encoder(chunk)
		bw_encoded_points.append(points)
		points_y = [po[1] for po in points]
		for y in points_y:
			bw_written_points += str(y) + "\n"

	with open(output_file, "w") as out_file:
		out_file.write(bw_written_points)

	print("Encoded to {} using error correction.".format(output_file))

	return bw_encoded_points

def berlekamp_welsh_encode(input_file, m, output_file):
	packets = split_message(input_file, m)
	encode(packets, N, K, P, output_file)
	print("Error correction encode successful.")
	print("__________________________")

if __name__ == "__main__":
	berlekamp_welsh_encode(dir_path+"encoded/500_char_encode.txt", 4, dir_path+"error_encoded/500_char_error_encode.txt")

	# encoder, decoder, _ = wb.makeEncoderDecoder(N, K, P)
	# a = [random.randint(0, P-1) for i in range(K-1)]
	# a.append(0)
	# print("original ", a)
	# e = encoder(a)
	# print("encode ", e)
	# d = [int(de) for de in decoder(e)]
	# print("decode ", d)
	# print(d == a)


