import parameters

file_name1 = parameters.receive_output
file_name2 = parameters.error_encode_output
file1 = open(file_name1, 'r')
file2 = open(file_name2, 'r')
	

arr1 = file1.readlines()
arr2 = file2.readlines()
print(len(arr1), len(arr2))
count = 0
total = 0
for i in range(min(len(arr1), len(arr2))):
		if arr1[i] != arr2[i]:
			count += 1
		total += 1
		if total % 131 == 0:
			print(count,total)
print(count)
file1.close()
file2.close()