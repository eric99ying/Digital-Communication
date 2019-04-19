import wave, struct, math, random, os, re
sampleRate = 44100.0 # hertz
duration = .048 # seconds

obj = wave.open('transmission.wav','w')
obj.setnchannels(1) # mono
obj.setsampwidth(2)
obj.setframerate(sampleRate)

def writeSinWave(freq, wav_obj):
   for i in range(int(sampleRate * duration)):
	   value = int(math.sin(2 * math.pi /(sampleRate/freq) * i) * 10000)
	   data = struct.pack('<h', value)
	   wav_obj.writeframesraw( data )

def get_freq_list(low, high, num_points):
	#returns list of num_points frequencies from low to high, with intervals defined by polynomial ax^2 + low.

	diff = high - low
	a = diff/((num_points - 1) * ((num_points - 1)))

	return [low + a * (i * i) for i in range(num_points)]

def read_message(input_file, low, high, num_points):
	freq_list = get_freq_list(low,high,num_points)
	with open(input_file, "r") as in_file:
		for line in in_file:
			b = int(line)
			writeSinWave(freq_list[b], obj)
	

read_message("../../error_encoded/500_char_error_encode.txt", 500, 7000, 17)
#print(get_freq_list(500,7000,17))




