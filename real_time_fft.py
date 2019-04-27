#record a sound and in real time display the frequency 
import numpy as np 
import pyaudio
import time
import matplotlib.pyplot as plt
import math
import parameters
from scipy.signal import find_peaks

def find_frequency(data, CHUNK):
	data = data * np.hanning(len(data)) #window data
	fft = abs(np.fft.fft(data).real) #returns some sort of complex array (coefficients are complex valued)
	fft = fft[:int(len(fft)/2)]
	freq = np.fft.fftfreq(CHUNK,1.0/RATE) #returns the highest frequency
	freq = freq[:int(len(freq)/2)] 
	freqDominant = freq[np.where(fft==np.max(fft))[0][0]] + 1
	freqSecondDominant = freq[np.where(fft==np.max(fft))[0][0]] + 1
	#conc = np.vstack((fft, freq))

	peaks, _ = find_peaks(fft, prominence=5000)
	
	l = []
	for peak in peaks:
		val = fft[peak]
		hz = abs(freq[peak])
		l.append( (val,hz) )
	
	if len(l) == 0:
		return freqDominant, 0
	elif len(l) == 1:
		l.append( (0,0) )
	l.sort(reverse=True)
	
	freqDominant = l[0][1]
	freqSecondDominant = l[1][1]

	#print(freqSecondDominant, freqDominant)
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
start_freq = 7500
start_window = 200
N = 100
CHUNK = parameters.CHUNK# number of data points to read at a time
RATE = 44100

def main():

	 # time resolution of the recording device (Hz)

	#begin = time.time()
	#alignment_buffer = 8
	#alignment_time = ((begin//alignment_buffer)+2) * alignment_buffer
	#print('begin', begin)
	#print('alignment_time', alignment_time)

	p=pyaudio.PyAudio()
	stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True, frames_per_buffer=CHUNK//10) #uses default input device
	freq_list = frequencies_array("frequencies.txt")

	#while time.time() < alignment_time:
	#	continue

	start_time = time.time()
	print('RECORDING STARTED', start_time)	# create a numpy array holding a single read of audio data
	frequency_array = []
	classify_array = []
	#timeout = time.time() + 10	 #10 seconds

	starting_flag = False
	prev_freq = -1
	count = 0
	buffer = np.array([])
	prev_start = False
	middle_flag = False
	#stream.start_stream()
	while True: 
		#adjust_time_start = time.time() 
		data = np.frombuffer(stream.read(CHUNK//10),dtype=np.int16)
		
		if starting_flag == False:
			frequency, second_freq = find_frequency(data, CHUNK//10)
			#print(frequency)
			if abs(frequency - start_freq) < start_window:
				prev_freq = 128
				if prev_start:
					starting_flag = True
					print("Starting frequency heard")
				prev_start = True
				count = 1
			else:
				prev_start = False
		elif middle_flag == False:
			frequency, second_freq = find_frequency(data, CHUNK//10)
			if frequency > 1300 and frequency < 6970:
				middle_flag = True
				buffer = np.append(buffer, data)
				count = 2
		
		elif count != 10:
			buffer = np.append(buffer, data)
			count += 1
		
		else:
			buffer = np.concatenate((buffer, data))
			frequency, second_freq = find_frequency(buffer, CHUNK)
			if frequency < 1000:
				frequency = second_freq
			
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
			count = 1
			buffer = np.array([])
		
	
	end_time = time.time()
	
	print('RECORDING ENDED', round(end_time, 5))
	
	print("Received ", len(classify_array), " points")
	#print('runtime of program:', end_time-start_time)
	# close the stream gracefully
	stream.stop_stream()
	stream.close()
	p.terminate()

	output_file = parameters.receive_output		


	if(len(classify_array) % parameters.N != 0):
		if (len(classify_array) % parameters.N > parameters.N/2):
			zeroes = np.zeros(parameters.N - len(classify_array) % parameters.N)
			classify_array = np.append(zeroes, classify_array)
		else:
			classify_array = classify_array[: - (len(classify_array) % parameters.N)]

	with open(output_file, 'w') as classify_file:
		for classification in classify_array:
			classify_file.write(str(classification) + '\n')

	classify_file.close()


	#print(frequency_array)

	




	

#sampling every 0.048 seconds

if __name__=="__main__":
	#frequencies_arr = frequencies_array("frequencies.txt")
	#classify = [classify_freq(freq, frequencies_arr) for freq in frequencies_arr]
	#print(classify)
	main()