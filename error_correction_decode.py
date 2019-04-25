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


NUM_SOUNDS = 16
N = 100
K = 50
P = 101

fp = FiniteField(P)

dir_path = os.path.dirname(os.path.abspath(__file__)) + "/"

############################
# LAGRANGE INTERPOLATION

# Multiply two polynomials together, returns list of coefficients
def mul_poly(poly1, poly2):
	deg1 = len(poly1)
	deg2 = len(poly2)
	final_poly = [fp(0)] * (deg1 + deg2 - 1)
	for i in range(len(poly1)):
		for j in range(len(poly2)):
			final_poly[i+j] = final_poly[i+j] + poly1[i]*poly2[j]
	return final_poly

# Add two polynomials together, returns list of coefficients
def add_poly(poly1, poly2):
	final_poly = [fp(0)] * max(len(poly1), len(poly2))
	for i in range(len(final_poly)):
		if i >= len(poly1):
			final_poly[i] = poly2[i]
		elif i >= len(poly2):
			final_poly[i] = poly1[i]
		else:
			final_poly[i] = poly2[i] + poly1[i]
	return final_poly

# Compute multiplicative inverse modulo a prime.
def inv(a, prime):
	return pow(a, prime-2, prime)

# Finds the coefficients of the langrage interpolated polynomial from the x, y points provided
def interpolate(xpoints, ypoints, prime):
	coefs = []
	for i in range(len(xpoints)):
		yi = ypoints[i]

		# calculate the denominator of the lagrange term
		res = []
		denom = fp(1)
		for j in range(len(xpoints)):
			if i != j:
				denom = denom * (xpoints[i] - xpoints[j])
		inv_denom = fp(inv(int(denom), prime))

		# calculate numerator
		res = [fp(1)]
		for j in range(len(xpoints)):
			if i != j:
				res = mul_poly(res, [-xpoints[j], 1])
		final_res = mul_poly(mul_poly(res, [inv_denom]), [yi])
		coefs = add_poly(coefs, final_res)

	return coefs



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
		try:
			dm = list(decoder(pp))
			print("B-W interp: ", dm)
			print("___________________________")
		except Exception as e:
			print("No solution found for B-W equations. Resorting to naive method.")
			received_points = pp
			random_chosen_points = []
			for _ in range(k):
			 	random_chosen = random.choice(received_points)
			 	received_points.remove(random_chosen)
			 	random_chosen_points.append(random_chosen)

			#random_chosen_points = received_points[1:k+1]

			xs = [x[0] for x in random_chosen_points]
			ys = [x[1] for x in random_chosen_points]
			lp = interpolate(xs, ys, p)
			dm = lp
			# print("Chosen points: ", random_chosen_points)
			print("Interpolated coefficients: ", dm)
			print("___________________________")


		while len(dm) < k:
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

	#berlekamp_welsh_decode(dir_path+"classify.txt", 4, dir_path+"error_decoded/error_decoded_classify.txt")
	# lp = interpolate([fp(1), fp(2), fp(3)], [fp(2), fp(3), fp(5)], 17)
	# print(lp)

