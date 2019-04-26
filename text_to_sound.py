import wave, struct, math, random, os, re
	
sampleRate = 44100.0 # hertz
CHUNK = 2117
end_duration = 44100.0
def make_wav_obj(sampleRate =sampleRate):

	obj = wave.open('Transmission/transmission.wav','w')
	obj.setnchannels(1) # mono
	obj.setsampwidth(2)
	obj.setframerate(sampleRate)
	return obj

def writeSinWave(freq, wav_obj):
   for i in range(CHUNK):
	   value = int(math.sin(2 * math.pi /(sampleRate/freq) * i) * 10000)
	   data = struct.pack('<h', value)
	   wav_obj.writeframesraw( data )

def get_freq_list(low, high, num_points):
	#returns list of num_points frequencies from low to high, with intervals defined by polynomial ax^2 + low.

	diff = high - low
	a = diff/(num_points - 1)
	"""a = diff/((num_points - 1) ** 1.5)

	arr = [low + a * (i ** 1.5) for i in range(num_points)]"""

	return [low + i *a for i in range(num_points)]


def construct_wav(input_file, low, high, num_points, obj):
	freq_list = get_freq_list(low,high,num_points)
	count = 0
	writeSinWave(7000, obj)
	with open(input_file, "r") as in_file:
		for line in in_file:
			b = int(line)
			count += 1
			writeSinWave(freq_list[b], obj)
	CHUNK = end_duration
	writeSinWave(7750, obj)
	print(count)
	
if __name__ == "__main__":
	obj = make_wav_obj()	
	construct_wav("error_encoded/500_char_error_encode.txt", 1500, 7000, 129, obj)
	
#print(get_freq_list(500,7000,17))




