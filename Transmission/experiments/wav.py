import wave, struct, math, random
sampleRate = 44100.0 # hertz
duration = .048 * 5 # seconds
frequency = 600.0 # hertz
obj = wave.open('sound.wav','w')
obj.setnchannels(1) # mono
obj.setsampwidth(2)
obj.setframerate(sampleRate)

def writeSinWave(freq, wav_obj):
   for i in range(int(sampleRate * duration)):
	   value = int(math.sin(2 * math.pi /(sampleRate/freq) * i) * 10000)
	   data = struct.pack('<h', value)
	   wav_obj.writeframesraw( data )



writeSinWave(600, obj)
writeSinWave(6000, obj)
writeSinWave(600, obj)
writeSinWave(6000, obj)
writeSinWave(600, obj)
writeSinWave(6000, obj)
writeSinWave(600, obj)
writeSinWave(6000, obj)
writeSinWave(600, obj)
writeSinWave(6000, obj)
