import pyaudio
import wave
import numpy as np
import sys
import time
from scipy.io import wavfile
def find_frequency(data):
	data = data * np.hanning(len(data)) #window data
	fft = abs(np.fft.fft(data).real) #returns some sort of complex array (coefficients are complex valued)
	fft = fft[:int(len(fft)/2)]
	freq = np.fft.fftfreq(CHUNK,1.0/RATE) #returns the highest frequency
	freq = freq[:int(len(freq)/2)] 
	freqDominant = freq[np.where(fft==np.max(fft))[0][0]] + 1
	return freqDominant

if __name__=="__main__":
	fs, data = wavfile.read('file.wav')
	search_length = 2205
	starting_frequency = 3000
	
	RATE = 44100
	CHUNK =2205

	print(len(data))
	removed_starting = False
	while not removed_starting:
		search_data = data[:search_length]
		freq = find_frequency(search_data)
		print(freq)
		if abs(freq - starting_frequency) < 100:
			data = data[search_length:]
		else:
			removed_starting = True
	print(len(data))

	"""frequencies = []
	i=0
	while i < len(data):
		current_sig = data[i:i+CHUNK]
		#print(len(current_sig))
		current_freq = find_frequency(current_sig)
		print(current_freq)
		#frequencies.append(current_freq)
		i += CHUNK"""

