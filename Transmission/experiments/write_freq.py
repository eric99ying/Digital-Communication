def write_freq_list(low, high, num_points):
	#returns list of num_points frequencies from low to high, with intervals defined by polynomial ax^2 + low.

	diff = high - low
	a = diff/((num_points - 1) ** 1.5)

	arr = [low + a * (i ** 1.5) for i in range(num_points)]

	f = open("frequencies.txt", "w")
	for i in arr:
		f.write(str(i) + "\r\n")
	f.close()
write_freq_list(1500,7000,17)


freq_list = [1500.0 ,1585.9375 ,1743.0679560328758,1946.5443488263513,2187.5,2460.810459081941,2763.0181486225765,3091.5847730622927,3444.5436482630057,3820.3125,4217.582364207201,4635.246872132839,5072.35479061081,5528.076815557426,6001.681543462399,6492.517594720498,7000.0]


def classify_freq(freq, freq_list= freq_list):
	if freq < freq_list[0]:
		return 0
	for i in range(1, len(freq_list)):
		if freq <= freq_list[i]:
			if(freq - freq_list[i-1] > freq_list[i] - freq):
				return i
			return i - 1
	return len(freq_list) - 1

print(classify_freq(1))

print(classify_freq(5342))

print(classify_freq(4234))

print(classify_freq(1253))

print(classify_freq(1342))

