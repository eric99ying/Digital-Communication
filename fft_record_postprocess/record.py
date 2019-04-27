def find_frequency(data):
	data = data * np.hanning(len(data)) #window data
	fft = abs(np.fft.fft(data).real) #returns some sort of complex array (coefficients are complex valued)
	fft = fft[:int(len(fft)/2)]
	freq = np.fft.fftfreq(CHUNK,1.0/RATE) #returns the highest frequency
	freq = freq[:int(len(freq)/2)] 
	freqDominant = freq[np.where(fft==np.max(fft))[0][0]] + 1
	fft = np.delete(fft, np.max(fft))
	freq = np.delete(freq, freqDominant - 1)
	#freqSecondDominant = freq[np.where(fft==np.max(fft))[0][0]] + 1
	return freqDominant
	
def writeSinWave(freq, wav_obj= obj):
   for i in range(int(sampleRate * duration)):
	   value = int(math.sin(2 * math.pi /(sampleRate/freq) * i) * 10000)
	   data = struct.pack('<h', value)
	   wav_obj.writeframesraw( data )

if __name__=="__main__":

	CHUNK = 2117# number of data points to read at a time
	RATE = 44100 # time resolution of the recording device (Hz)

	p=pyaudio.PyAudio()
	stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True, frames_per_buffer=CHUNK) #uses default input device
	freq_list = frequencies_array("frequencies.txt")


	start_time = time.time()
	print('RECORDING STARTED', start_time)	# create a numpy array holding a single read of audio data
	frequency_array = []
	classify_array = []
	#timeout = time.time() + 10  #10 seconds

	starting_flag = False
	prev_freq = -1
	count = 0
	#stream.start_stream()
	while True: 
		#adjust_time_start = time.time() 
		data = np.frombuffer(stream.read(CHUNK),dtype=np.int16)
		frequency, second_freq = find_frequency(data)
		classified_frequency = classify_freq(frequency, freq_list)

		if classified_frequency == prev_freq:
			classified_frequency = classify_freq(second_freq, freq_list)

		
		if abs(frequency - end_freq) < end_window:
			print("Ending frequency heard")
			break
		
		frequency_array.append(classified_frequency)
		if starting_flag:
			classify_array.append(classified_frequency)

		if abs(frequency - start_freq) < start_window:
			if starting_flag == False:
				print("Starting frequency heard")
				prev_freq = 100
			starting_flag = True
		prev_freq = classified_frequency

		
	
	end_time = time.time()
	
	print('RECORDING ENDED', round(end_time, 5))
	
	print("Received ", len(classify_array), " points")
	#print('runtime of program:', end_time-start_time)
	# close the stream gracefully
	stream.stop_stream()
	stream.close()
	p.terminate()

	output_file = 'classify.txt'



	with open(output_file, 'w') as classify_file:
		for classification in classify_array:
			classify_file.write(str(classification) + '\n')

	classify_file.close()


	#print(frequency_array)

	