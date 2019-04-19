#record a sound and in real time display the frequency 
import numpy as np 
import pyaudio
import time

#sampling every 0.09287 seconds

CHUNK = 4096 # number of data points to read at a time
RATE = 44100 # time resolution of the recording device (Hz)

p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK) #uses default input device
start_time = time.process_time()
print('RECORDING STARTED', start_time)
# create a numpy array holding a single read of audio data

timeout = time.time() + 10  #10 seconds

while time.time() < timeout: #to it a few times just to see
    data = np.frombuffer(stream.read(CHUNK),dtype=np.int16)
    print(data)
end_time = time.process_time()

print('RECORDING ENDED', end_time)
#print('runtime of program:', end_time-start_time)
# close the stream gracefully
stream.stop_stream()
stream.close()
p.terminate()