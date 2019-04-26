'''
parameters.py
~~~
Contains all adjustable parameters in our system.
'''

# Berlekamp-Welch
N = 129
K = 100
P = 131

# Number of bits to group by
group = 7


# Files written to
input_text_file = "tests/test25.txt"
huffman_encode_output = "encoded/test25.txt"
error_encode_output = "error_encoded/test25.txt"

receive_output = "received/test25.txt"
error_decode_output = "error_decoded/test25.txt"
huffman_decode_output = "decoded/test25.txt"
