#record a sound and in real time display the frequency 
import numpy as np 
import pyaudio
import time
import matplotlib.pyplot as plt

def find_frequency(data):
	data = data * np.hanning(len(data)) #window data
	fft = abs(np.fft.fft(data).real) #returns some sort of complex array (coefficients are complex valued)
	fft = fft[:int(len(fft)/2)]
	freq = np.fft.fftfreq(CHUNK,1.0/RATE) #returns the highest frequency
	freq = freq[:int(len(freq)/2)] 
	freqDominant = freq[np.where(fft==np.max(fft))[0][0]]+1
	#plot(freq, fft)
	return freqDominant

def plot(freq, fft_coeffs): #freq vs fft coefficients
	plt.plot(freq,fft_coeffs)
	plt.axis([0,4000,None,None])
	plt.show()
	plt.close()

#sampling every 0.09287 seconds
if __name__=="__main__":
	CHUNK = 4410 # number of data points to read at a time
	RATE = 44100 # time resolution of the recording device (Hz)

	p=pyaudio.PyAudio()
	stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True, frames_per_buffer=CHUNK) #uses default input device
	start_time = time.time()
	print('RECORDING STARTED', 0)
	# create a numpy array holding a single read of audio data

	frequency_array = []
	timeout = time.time() + 10  #10 seconds

	while time.time() < timeout: #to it a few times just to see
		#adjust_time_start = time.time() 
		data = np.frombuffer(stream.read(CHUNK),dtype=np.int16)
		frequency = find_frequency(data)
		frequency_array.append(frequency)
		print("dominant frequency: %d Hz"%frequency)

		#adjust_time_end = time.time()
		#difference = adjust_time_end - adjust_time_start
		#print(difference)
		#timeout -=difference
	    #print(data)
		
	
	end_time = time.time()

	print('RECORDING ENDED', round(end_time-start_time, 5))
	#print('runtime of program:', end_time-start_time)
	# close the stream gracefully
	stream.stop_stream()
	stream.close()
	p.terminate()

	#print(frequency_array)


#def frequency_to_bits(frequency_array):

	
