'''
huffman_encode_2.py
~~~
Takes in a text file and encodes it into 1's and 0's using Huffman Encoding. 
'''
import os
import heapq
import re
import binascii

dir_path = os.path.dirname(os.path.abspath(__file__)) + "/"

def convert_ascii_bin(ascii_str):
	'''
	Converts an ascii string to binary.
	'''
	output_str = ""
	for c in ascii_str:
		output_str += bin(ord(c))[2:]
	return output_str


def create_freq_dict(input_file):
	'''
	Takes in input file and creates huffman dictionary from it.

	Args:
		input_file (str): The file of text.
	Returns:
		dict: The dictionary of ascii characters and frequency values

	'''
	freq_dict = {}
	with open(dir_path + input_file, "r") as in_file:
		text = in_file.read()
		bin_str = convert_ascii_bin(text)
		i = 0
		while:
			
			i += 16
	return freq_dict

def create_huffman_dictionary(freq_dict):
	'''
	Takes in a frequncy dictionary of ascii characters and creates a huffman dictionary from it.

	Args:
		freq_dict (dict): The dictionary detailing the frequencies of each ascii character.
	Returns;
		dict: The huffman dictionary mapping each ascii character to a bitstring.
	'''
	pq = []  #Stores tuples of (weight, [ascii_chars...]), orders by weight
	huff_dict = {}
	for k in freq_dict.keys():
		heapq.heappush(pq, (freq_dict[k], [k]))
		huff_dict[k] = ""

	# Repeatedly combine lowest weighted nodes into supernodes
	while (len(pq) >= 2):
		tuple_1 = heapq.heappop(pq)
		tuple_2 = heapq.heappop(pq)
		combined_tuple = (tuple_1[0] + tuple_2[0], tuple_1[1] + tuple_2[1])
		for k in tuple_2[1]:
			huff_dict[k] = "1" + huff_dict[k]
		for k in tuple_1[1]:
			huff_dict[k] = "0" + huff_dict[k]
		heapq.heappush(pq, combined_tuple)

	return huff_dict

def huffman_encode(text_file, output_file, huffman_dict):
	'''
	Encodes a text file and writes to an output file using the huffman dictionary.

	Args:
		text_file (str): The name of text file in same directory.
		output_file (str): The name of output file to write to.
		huffman_dict (dict): The huffman dictionary to use for encoding
	Returns:
		None

	'''
	with open(dir_path + text_file, "r") as in_file, open(dir_path + output_file, "w") as out_file:
		text_string = in_file.read()
		output_str = ""
		for c in text_string:
			output_str += huffman_dict[c]

		out_file.write(output_str)

	print("Encoded text file written to ", output_file)


def convert(text_file, output_file, freq_file):
	'''
	Takes text_file, huffman encodes it according to the frequency in freq_file, and writes to output_file.
	'''
	freq_dict = create_freq_dict(freq_file)
	huffman_dict = create_huffman_dictionary(freq_dict)
	huffman_encode(text_file, output_file, huffman_dict)

	print("Phase 1: Encoding Success")
	print("__________________________")

if __name__ == "__main__":

	print(convert_ascii_bin("adfosfisodf"))

	#convert("tests/TextFile1.txt", "encoded/EncodeFile1.txt", "ascii_frequency.txt")

