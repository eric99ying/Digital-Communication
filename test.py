import pyaudio
import wave
import sys
import time
import math

CHUNK = 2117
file_name = "Transmission/transmission.wav"



def play_wav(file_name = file_name):
	start_time = time.time()
	
	wf = wave.open(file_name, 'rb')

	# instantiate PyAudio (1)
	p = pyaudio.PyAudio()

	# open stream (2)
	stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
	                channels=wf.getnchannels(),
	                rate=wf.getframerate(),
	                output=True)

	# read data
	data = wf.readframes(CHUNK)

	# play stream (3)
	while len(data) > 0:
	    stream.write(data)
	    data = wf.readframes(CHUNK)

	# stop stream (4)
	stream.stop_stream()
	stream.close()

	# close PyAudio (5)
	p.terminate()

if __name__ == "__main__":
		play_wav(file_name)