'''
huffman_decode
~~~
Takes in a file containing binary numbers and decodes it into ascii characters.

'''

import os
import re
import heapq
import operator


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

class HuffNode:
	'''
	A node in the huffman binary tree.
	'''
	label = ""
	left = None
	right = None
	freq = 0
	def __init__(self, label, freq, left = None, right = None):
		'''
		Constructor for the HuffNode.
		'''
		self.left = left
		self.right = right
		self.freq = freq
		self.label = label

	def isLeaf(self):
		'''
		Returns if the current node is leaf.
		'''
		return self.left == None and self.right == None

	def __str__(self):
		return "[{}, [{}, {}]]".format(self.label, self.left.__str__(), self.right.__str__())
	
	
def create_huffman_tree(freq_dict):
	'''
	Creates a huffman tree from the provided freq_dict.

	Args:
		freq_dict (dict): The provided frequency dictionary.
	Returns:
		HuffNode: The root node of the huffman tree
	'''
	# (1) Create huffnode_dict which stores mapping between labels(ascii char) and HuffNode
	huffnode_dict = {}
	for key,value in freq_dict.items():
		huffnode_dict[str(key)] = HuffNode(int(key), float(value))
	#print(huffnode_dict)
	sorted_items = sorted(freq_dict.items(), key=operator.itemgetter(1))
	
	# (2) Create a heap storing (weight, HuffNode)
	heap_elts = [(float(i[1]), str(i[0])) for i in sorted_items]
	heapq.heapify(heap_elts)
	num_supernodes = 0
	while(len(heap_elts)) > 1:
		# (3) Create super HuffNodes from the two lowest weight nodes and repush into the heap
		min1 = heapq.heappop(heap_elts)
		min2 = heapq.heappop(heap_elts)
		min1 = huffnode_dict[min1[1]]
		min2 = huffnode_dict[min2[1]]
		freq_sum = float(min1.freq + min2.freq)
		super_label = "super " + str(num_supernodes)
		supernode = HuffNode(super_label, freq_sum, min1, min2)
		huffnode_dict[super_label] = supernode
		heapq.heappush(heap_elts, (float(freq_sum), super_label))
		num_supernodes += 1

	# (4) Return the supernode, which corresponds to the root node of Huffman tree
	return supernode

def decode(input_file, output_file, huffman_tree):
	'''
	Decodes a binary input_file into a output_file.

	Args:
		input_file (str): The text file of the input file.
		output_file (str): The text file of the output file.
		huffman_tree (HuffNode): The root node of the huffman tree.
	Returns:
		None

	'''
	with open(dir_path + input_file, "r", encoding="utf-8") as in_file, open(dir_path + output_file, "w") as out_file:
		tracker = huffman_tree
		bin_str = in_file.read()
		output_str = ""
		for bit in bin_str:
			if bit == '0':
				tracker = tracker.left
			elif bit == '1':
				tracker = tracker.right
			else:
				raise Exception("Invalid bit found in binary file.")
			if tracker.isLeaf():
				#print("found:", tracker.label)
				output_str += chr(int(tracker.label))
				tracker = huffman_tree
		out_file.write(output_str)

	print("Decoded text written to ", output_file)

def devert(bin_file, output_file, freq_file):
	'''
	Takes binary_file, huffman decodes it according to the frequency in freq_file, and writes to output_file.
	'''
	freq_dict = create_freq_dict(freq_file)
	huffman_tree = create_huffman_tree(freq_dict)

	decode(bin_file, output_file, huffman_tree)

	print("Huffman Decoding Success")
	print("__________________________")


if __name__ == "__main__":
	#devert("encoded/EncodeFile4.txt", "decoded/DecodeFile4.txt", "frequency_table_2.txt")
	devert("error_decoded/error_decoded_classify.txt", "decoded/shorttest.txt", "frequency_table_2.txt")



