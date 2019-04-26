import pyaudio
import wave
import sys
import time
import math

CHUNK = 1024

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s feel_good_x.wav" % sys.argv[0])
    sys.exit(-1)

start_time = time.time()
	
wf = wave.open(sys.argv[1], 'rb')

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# open stream (2)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

# read data
data = wf.readframes(CHUNK)

#time_buffer = 8
#end_time = (((start_time // time_buffer) + 2) * time_buffer)
#while time.time() < end_time:
	#continue

#print(start_time)
#print(end_time)
#print(time.time())

# play stream (3)
while len(data) > 0:
    stream.write(data)
    data = wf.readframes(CHUNK)

# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()