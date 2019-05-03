'''
parameters.py
~~~
Contains all adjustable parameters in our system.
'''

# Berlekamp-Welch
N = 129
K = 64
P = 131

# Number of bits to group by
group = 7

# Duration each sound is played
CHUNK = 2570

# Files written to
input_text_file = "tests/demo-test.txt"
huffman_encode_output = "encoded/demo-test.txt"
error_encode_output = "error_encoded/demo-test.txt"

receive_output = "received/demo-test.txt"
error_decode_output = "error_decoded/demo-test.txt"
huffman_decode_output = "decoded/demo-test.txt"
