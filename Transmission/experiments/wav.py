import wave, struct, math, random
sampleRate = 44100.0 # hertz
duration = 1 # seconds
frequency = 440.0 # hertz
obj = wave.open('sound.wav','w')
obj.setnchannels(1) # mono
obj.setsampwidth(2)
obj.setframerate(sampleRate)

def writeSinWave(freq, wav_obj):
   for i in range(int(sampleRate * duration)):
	   value = int(math.sin(2 * math.pi /(sampleRate/freq) * i) * 10000)
	   data = struct.pack('<h', value)
	   wav_obj.writeframesraw( data )

writeSinWave(frequency, obj)

frequency = 900.0
writeSinWave(frequency, obj)

frequency = 10300.0
writeSinWave(frequency, obj)

frequency = 20000.0
writeSinWave(frequency, obj)

frequency = 3000.0
writeSinWave(frequency, obj)

frequency = 900.0
writeSinWave(frequency, obj)

frequency = 1300.0
writeSinWave(frequency, obj)

frequency = 2000.0
writeSinWave(frequency, obj)

frequency = 3000.0
writeSinWave(frequency, obj)


frequency = 900.0
writeSinWave(frequency, obj)

frequency = 1300.0
writeSinWave(frequency, obj)

frequency = 2000.0
writeSinWave(frequency, obj)

frequency = 30000.0
writeSinWave(frequency, obj)



