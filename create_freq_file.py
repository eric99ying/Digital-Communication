'''
Script to read a large text file and create a frequency table of ascii characters. Converts chars to ints 
using ord(). Use chr() to convert back.
'''

import os
import re
from collections import OrderedDict
from operator import itemgetter



dir_path = os.path.dirname(os.path.abspath(__file__)) + "/"
data_file = dir_path + "dataset/prideandprejudice.txt"
output = dir_path + "frequency_table_2.txt"

count = {}
out_str = []
with open(data_file, "r", encoding="utf-8") as in_file, open(output, "w") as out_file:
	c = in_file.read(1)
	while(c):
		c = ord(c)
		if c in count.keys():
			count[c] = count[c] + 1
		else:
			count[c] = 1
		c = in_file.read(1)


	newcount = OrderedDict(sorted(count.items(), key=itemgetter(1), reverse=True))
	for k, v in newcount.items():
		if k == "\n":
			out_str.append("\\n     {}\n".format(v))
		else:
			out_str.append("{}     {}\n".format(k, v))

	out_file.writelines(out_str)

print("Number of unique characters: ", len(count))
print("Frequency table created")
