import csv
import numpy as np
import sys

def reject_outliers(data):
	Q1 = np.percentile(data, 25, interpolation = 'midpoint') 

	Q3 = np.percentile(data, 75, interpolation = 'midpoint') 
	IQR = Q3 - Q1
	upper_bound = Q3 + 1.5*IQR
	lower_bound = Q1 - 1.5*IQR

	# Upper bound
	data = data[(data < upper_bound) & (data > lower_bound)]
  
	return data


with open('accesses.raw.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0
	previous = 0
	count = 0
	first_loop = False
	differences = np.array([])
	counts = np.array([])
	for row in csv_reader:
		
		if(row[4] == "GEMM"):
			previous = int(row[0])
			first_loop = False
			counts = np.append(counts,count)
			count = 0

		elif(row[4] == "Inner loop"):
			first_loop = True
		elif(row[4] == "Inner loop2"):
			if(first_loop):
				count += 1

			first_loop = False
		else: #(row[4] == "Conv"):
			if(previous > 0):
				differences = np.append(differences,int(row[0]) - previous)
			previous = 0
			count = 0
			first_loop = False

	#print(differences)
	#print("75% Percentile:", np.percentile(differences,75), "Median:", np.median(differences), "25% Percentile:", np.percentile(differences,25), "Standard deviation:", np.std(differences))
	if len(differences) < 4:
		print("X,X")
		sys.exit()
	
	differences = reject_outliers(differences)
	#print(counts)

	counts = counts[counts != 0]
	#counts = reject_outliers(counts)
	#print(differences)
	print("{0},{1},{2}".format(np.mean(differences), np.std(differences), np.mean(counts)))
	#print("{0},{1}".format(np.mean(differences), np.std(differences)))
