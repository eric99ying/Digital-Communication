import wave, struct, math, random
sampleRate = 44100.0 # hertz
duration =    1 * .048 # seconds
frequency = 600.0 # hertz
obj = wave.open('sound.wav','w')
obj.setnchannels(1) # mono
obj.setsampwidth(2)
obj.setframerate(sampleRate)

duration = 0.01

def writeSinWave(freq, wav_obj = obj):
   for i in range(int(sampleRate * duration)):
	   value = int(math.sin(2 * math.pi /(sampleRate/freq) * i) * 10000)
	   data = struct.pack('<h', value)
	   wav_obj.writeframesraw( data )

freq_list = [1500.0 ,1585.9375 ,1743.0679560328758,1946.5443488263513,2187.5,2460.810459081941,2763.0181486225765,3091.5847730622927,3444.5436482630057,3820.3125,4217.582364207201,4635.246872132839,5072.35479061081,5528.076815557426,6001.681543462399,6492.517594720498,7000.0]

writeSinWave(7000)
duration = 0.048
for i in freq_list:
	writeSinWave(i)
duration = 1
writeSinWave(7750)
