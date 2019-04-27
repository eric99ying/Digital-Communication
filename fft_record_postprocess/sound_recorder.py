import pyaudio
import wave
import numpy as np
import sys
import time

def find_frequency(data):
	data = data * np.hanning(len(data)) #window data
	fft = abs(np.fft.fft(data).real) #returns some sort of complex array (coefficients are complex valued)
	fft = fft[:int(len(fft)/2)]
	freq = np.fft.fftfreq(CHUNK,1.0/RATE) #returns the highest frequency
	freq = freq[:int(len(freq)/2)] 
	freqDominant = freq[np.where(fft==np.max(fft))[0][0]] + 1
	#fft = np.delete(fft, np.max(fft))
	#freq = np.delete(freq, freqDominant - 1)
	#freqSecondDominant = freq[np.where(fft==np.max(fft))[0][0]] + 1
	return freqDominant

if __name__=="__main__":
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 44100
	CHUNK = 2205
	RECORD_SECONDS = float(sys.argv[1])
	WAVE_OUTPUT_FILENAME = "file.wav"
	 
	audio = pyaudio.PyAudio()
	 
	# start Recording
	stream = audio.open(format=FORMAT, channels=CHANNELS,
	                rate=RATE, input=True,
	                frames_per_buffer=CHUNK)
	print ("recording...")
	frames = []

	starting_frequency = 3000
	#ending_frequency = 7000
	error_allowed = 50
	started = False
	ended = False
	starting_time = float("inf")
	while time.time() < RECORD_SECONDS + starting_time:
	    data = np.frombuffer(stream.read(CHUNK),dtype=np.int16)
	    #prior to starting
	    if not started:
	    	frequency = find_frequency(data)
	    	print(frequency)
	    	if abs(frequency - starting_frequency) < error_allowed:
	    		print("started")
	    		started = True
	    		frames.append(data)
	    		starting_time = time.time()
	    #during recording
	    else:
	    	frames.append(data)


	print ("finished recording")

	# stop Recording
	stream.stop_stream()
	stream.close()
	audio.terminate()
	 
	waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	waveFile.setnchannels(CHANNELS)
	waveFile.setsampwidth(audio.get_sample_size(FORMAT))
	waveFile.setframerate(RATE)
	waveFile.writeframes(b''.join(frames))
	waveFile.close()