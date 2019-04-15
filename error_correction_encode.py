'''
error_correction.py
~~~
Corrects errors in tranmission of bits through Reed Soloman and Berlekemp-Welsh.
'''

from berlekamp-welsh import welshberlekamp as wb

dir_path = os.path.dirname(os.path.abspath(__file__)) + "/"

p = 16

def split_message(input_file, k):
	'''
	Takes in an input file consisting of binary bits and splits it into groups of k bits.

	Args:
		input_file (str): The name of input file.
		k (int): The number of bits to split by.
	Return
	'''
	bits = []
	track = 0
	num_bits_sofar = 0
	with open(dir_path + input_file, "r") as in_file:
		b = in_file.read(1)
		while b:
			track = track*2 + int(b)
			num_bits_sofar += 1
			if num_bits_sofar > k:
				bits.append(track)
				num_bits_so_far = 0
				track = 0
			b = in_file.read(1)
		while num_bits_sofar < k:
			track = track*2
			num_bits_sofar += 1
		bits.append(track)

	


wb.makeEncoderDecoder()