def write_freq_list(low, high, num_points):
	#returns list of num_points frequencies from low to high, with intervals defined by polynomial ax^2 + low.

	diff = high - low
	a = diff/(num_points - 1)
	"""a = diff/((num_points - 1) ** 1.5)

	arr = [low + a * (i ** 1.5) for i in range(num_points)]"""

	arr = [low + i *a for i in range(num_points)]


	f = open("frequencies.txt", "w")
	for i in arr:
		f.write(str(i) + "\r\n")
	f.close()
write_freq_list(1500,7000,131)


def classify_freq(freq, freq_list= freq_list):
	if freq < freq_list[0]:
		return 0
	for i in range(1, len(freq_list)):
		if freq <= freq_list[i]:
			if(freq - freq_list[i-1] > freq_list[i] - freq):
				return i
			return i - 1
	return len(freq_list) - 1

