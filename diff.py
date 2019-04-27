file_name1 = "received/classify.txt"
file_name2 = "error_encoded/test25.txt"
file1 = open(file_name1, 'r')
file2 = open(file_name2, 'r')
	

arr1 = file1.readlines()
arr2 = file2.readlines()
print(len(arr1), len(arr2))
count = 0
for i in range(min(len(arr1), len(arr2))):
		if arr1[i] != arr2[i]:
			count += 1
print(count)
file1.close()
file2.close()