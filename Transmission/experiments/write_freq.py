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
