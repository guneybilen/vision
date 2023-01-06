import difflib


class VideoWriter:

	@staticmethod
	def comparer():
		
		with open("video1.txt", "r") as file_1:
			file_1_text = file_1.readlines()

		with open("video2.txt", "r") as file_2:
			file_2_text = file_2.readlines()
			
		for line in difflib.unified_diff(
			file_1_text, file_2_text, fromfile="file1.txt", tofile="file2.txt", lineterm=''
		):	
			h=open("video3.txt", "a")	
			h.write(str(h))
			h.close()
