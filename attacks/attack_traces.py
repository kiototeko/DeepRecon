import csv
import numpy as np
import operator

with open('accesses.raw.csv') as csv_file, open('database.csv') as database:
	csv_reader = csv.reader(csv_file, delimiter=',')
	database_reader = csv.reader(database, delimiter=',')
	sortedlist = sorted(database_reader, key=lambda row: float(row[2]))
	previous = 0
	differences = np.array([])
	for row in csv_reader:
		if(row[4] == "GEMM"):
			previous = int(row[0])
		elif("Inner loop" in row[4]):
			continue
		else: #elif(row[4] == "Conv"):
			if(previous > 0):
				differences = np.append(differences,int(row[0]) - previous)
			previous = 0
		"""
		else:
			previous = 0
		"""

	parameters = []
	for sample in differences:
		for k,row in enumerate(sortedlist):
			if(sample <= float(row[2])):
				if(k == 0):
					parameters.append(k)
				else:
					diff_next = float(row[2]) - sample
					diff_prev = sample - float(sortedlist[k-1][2])
					if(diff_next > diff_prev):
						parameters.append(k-1)
					else:
						parameters.append(k)
				break
					
	for k,i in enumerate(parameters):
		print("Sample:", differences[k], "Kernel size:", sortedlist[i][0], "Input channels:", sortedlist[i][1], "Reference mean time:", sortedlist[i][2])		
