'''
error_correction_decode.py
~~~
Perform berlekamp-welsh to decode the encoded transmitted bits. Writes to an output file. 

message-> huffman_encode -> error_correction_encode -> transmission -> receive 
-> error_correction_decode -> huffman_decode -> retrieved message
'''
import os
import random
import re
from berlekamp_welsh import welchberlekamp as wb
from berlekamp_welsh.finitefield.finitefield import FiniteField

N = 16
K = 12
P = 17

fp = FiniteField(P)

dir_path = os.path.dirname(os.path.abspath(__file__)) + "/"

############################
# LAGRANGE INTERPOLATION

def inv(a, prime):
    """
    Compute multiplicative inverse modulo a prime.
    """
    return pow(a, prime-2, prime)


def interpolate(points, prime):
    if type(points) is list and all([type(p) is int for p in points]):
        points = dict(zip(range(1,len(points)+1), points))
    elif type(points) in [list,set,tuple] and\
       len(points) > 0 and\
       all([type(p) in [list,tuple] and len(p) == 2 for p in points]):
        points = dict([tuple(p) for p in points])
    elif type(points) is dict:
        pass
    else:
        raise TypeError("Expecting a list of values, list of points, or a mapping.")

    if type(prime) != int or prime <= 1:
        raise ValueError("Expecting a prime modulus.")

    # Compute the Langrange coefficients at 0.
    coefficients = {}
    for i in range(1, len(points)+1):
      coefficients[i] = 1
      for j in range(1, len(points)+1):
        if j != i:
          coefficients[i] = (coefficients[i] * (0-j) * inv(i-j, prime)) % prime

    value = 0
    print("P: ", points)
    print("C: ", coefficients)
    for i in range(1, len(points)+1):
      value = (value + points[i] * coefficients[i]) % prime

    return value, coefficients


############################


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
	print("Number of points received: ", len(packets))
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
		pp = points[i:i+n]
		print("Num points on polynomial: ", len(pp))
		# print("Points on polynomial: ", pp)
		try:
			dm = list(decoder(pp))
		except Exception as e:
			print("No solution found for B-W equations. Resorting to naive method.")
			received_points = pp
			random_chosen_points = []
			# for _ in range(k):
			# 	random_chosen = random.choice(received_points)
			# 	received_points.remove(random_chosen)
			# 	random_chosen_points.append(random_chosen)

			random_chosen_points = received_points[1:k+1]

			xs = [int(x[0]) for x in random_chosen_points]
			ys = [int(x[1]) for x in random_chosen_points]
			lp = list(interpolate(list(zip(xs, ys)), p)[1])
			dm = lp
			print("dm: ", dm)

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
	berlekamp_welsh_decode(dir_path+"classify.txt", 4, dir_path+"error_decoded/error_decoded_classify.txt")


