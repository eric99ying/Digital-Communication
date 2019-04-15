'''
huffman_encode.py
~~~
Takes in a text file and encodes it into 1's and 0's using Huffman Encoding. 
'''
import os
import heapq
import re
import math
import binascii

dir_path = os.path.dirname(os.path.abspath(__file__)) + "/"

def create_freq_dict(freq_file):
	'''
	Takes in a file containing frequencies of ascii characters and frequency values, and creates a 
	dictionary from it.

	Args:
		freq_file (str): The file of frequencies. Found from:
			https://reusablesec.blogspot.com/2009/05/character-frequency-analysis-info.html
	Returns:
		dict: The dictionary of ascii characters and frequency values

	'''
	freq_dict = {}
	with open(dir_path + freq_file, "r") as in_file:
		line = in_file.readline()
		while line:
			# Check that line contains ascii char and frequency
			ascii_char = int((re.search("^(\d+) ", line).groups()[0]))
			ascii_freq = float(re.search("  ([\d.]+)", line).groups()[0])
			freq_dict[ascii_char] = ascii_freq

			line = in_file.readline()

	freq_dict[126] = 1.    # ~ corresonds to characters that do not exist in frequency table
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
	with open(dir_path + text_file, "r", encoding="utf-8-sig") as in_file, open(dir_path + output_file, "w") as out_file:
		text_string = in_file.read()
		output_str = ""
		for c in text_string:
			try:
				output_str += huffman_dict[ord(c)]
			except KeyError as err:
				output_str += huffman_dict[126]

		out_file.write(output_str)


	print("Length of original text: ", len(text_string)*8)
	print("Length of encoded text: ", len(output_str))
	print("Encoded text file written to ", output_file)


def convert(text_file, output_file, freq_file):
	'''
	Takes text_file, huffman encodes it according to the frequency in freq_file, and writes to output_file.
	'''
	freq_dict = create_freq_dict(freq_file)
	print(freq_dict)
	huffman_dict = create_huffman_dictionary(freq_dict)
	print(huffman_dict)
	huffman_encode(text_file, output_file, huffman_dict)

	total_sum = sum([f for f in freq_dict.values()])
	entropy = -sum([(f/total_sum)*math.log(f/total_sum) for f in freq_dict.values()])
	print("Entropy: ", entropy)
	print("Phase 1: Encoding Success")
	print("__________________________")

if __name__ == "__main__":

	convert("tests/test3.txt", "encoded/EncodeFile4.txt", "frequency_table_2.txt")

