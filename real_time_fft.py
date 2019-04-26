#record a sound and in real time display the frequency 
import numpy as np 
import pyaudio
import time
import matplotlib.pyplot as plt
import math

def find_frequency(data):
	data = data * np.hanning(len(data)) #window data
	fft = abs(np.fft.fft(data).real) #returns some sort of complex array (coefficients are complex valued)
	fft = fft[:int(len(fft)/2)]
	freq = np.fft.fftfreq(CHUNK,1.0/RATE) #returns the highest frequency
	freq = freq[:int(len(freq)/2)] 
	freqDominant = freq[np.where(fft==np.max(fft))[0][0]] + 1
	freqSecondDominant = freq[np.where(fft==np.max(fft))[0][0]] + 1
	##print(freqSecondDominant, freqDominant)
	#plot(freq, fft)
	return freqDominant, freqSecondDominant

def plot(freq, fft_coeffs): #freq vs fft coefficients
	plt.plot(freq,fft_coeffs)
	plt.axis([0,4000,None,None])
	plt.show()
	plt.close()

def frequencies_array(file_name):
	file1 = open(file_name, 'r')
	

	freq_array = file1.readlines()
	file1.close()
	freq_array_int = []
	for elem in freq_array:
		if elem[:len(elem)-3] != '':
			freq_array_int.append(float(elem[:len(elem)-3]))
	return freq_array_int

def classify_freq(freq, freq_list):
	if freq < freq_list[0]:
		return 0
	for i in range(1, len(freq_list)):
		if freq <= freq_list[i]:
			if(freq - freq_list[i-1] > freq_list[i] - freq):
				return i
			return i - 1
	return len(freq_list) - 1

def start_frequency(test_freq, frequencies_array):
	for freq in frequencies_array:
		if abs(freq-test_freq) < 15:
			return True
	return False



end_freq = 7750
end_window = 50
start_freq = 7000
start_window = 50
N = 100

#sampling every 0.048 seconds
if __name__=="__main__":
	#frequencies_arr = frequencies_array("frequencies.txt")
	#classify = [classify_freq(freq, frequencies_arr) for freq in frequencies_arr]
	#print(classify)

	CHUNK = 2117 * 2# number of data points to read at a time
	RATE = 44100 # time resolution of the recording device (Hz)

	#begin = time.time()
	#alignment_buffer = 8
	#alignment_time = ((begin//alignment_buffer)+2) * alignment_buffer
	#print('begin', begin)
	#print('alignment_time', alignment_time)

	p=pyaudio.PyAudio()
	stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True, frames_per_buffer=CHUNK) #uses default input device
	freq_list = frequencies_array("frequencies.txt")

	#while time.time() < alignment_time:
	#	continue

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
			#print("Raw freq", frequency)
			"""if (abs(frequency - second_freq) < 40):
				print(frequency, second_freq)
				count += 1"""

		if abs(frequency - start_freq) < start_window:
			if starting_flag == False:
				print("Starting frequency heard")
				prev_freq = 128
			starting_flag = True
		prev_freq = classified_frequency
		#if (abs(frequency-7000) < 5):
		
		#print("actual freq: %d"%frequency)
		#print("classified freq: %d"%classify_freq(frequency, freq_list))

		#start frequency 
		

		#adjust_time_end = time.time()
		#difference = adjust_time_end - adjust_time_start
		#print(difference)
		#timeout -=difference
	    #print(data)
		
	
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

	




	
