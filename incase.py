for root, dirs, files in os.walk(dir_path):
	for dir in dirs:
		for file in files:
			if file.endswith(ext):
				test_string = file.split(".")[0]
				#print(test_string)
				eph = re.findall(r'\s+', test_string)
				print(eph)
				temp = re.findall(r'\d+', test_string)
				ary.append(temp)
				flatten_list = list(deepflatten(ary))
				flattened = [int(e) for e in flatten_list]	
				sorted_list_biggest=sorted(flattened)[-1]

counter = sorted_list_biggest + 1
