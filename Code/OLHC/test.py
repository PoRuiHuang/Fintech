
import csv
import numpy as np
import sys
# 開啟 CSV 檔案
# row  = []
# row2 = []
CSV = sys.argv[1]
with open(CSV, encoding = 'big5' ) as csvfile:
  # 讀取 CSV 檔案內容
	arr = csv.reader(csvfile)
	date = 0
	count = 0
	for row  in arr:
		if count == 0:
			count +=1
		else: 
			if int(row[0]) > date:
				date = int(row[0])
  		# row.append(row)
# print(row[0])
# row = np.roway(row) #要刪東西前再np.roway


# for i in range(len(row)):		
if date<=20190821:
	standard = "201908"
elif date<=20190918:
	standard = "201909"
elif date<=20191016:
	standard = "201910"

MIN = 134500
MAX = 84500
H = 0
L = 99999
with open(CSV, encoding = 'big5' ) as csvfile:
  # 讀取 CSV 檔案內容
	arr = csv.reader(csvfile)
	for row  in arr:
		if row[1].rstrip() == "TX" and str(row[2]).rstrip() == standard and int(row[3]) >= 84500 and int(row[3]) <= 134500:
			if int(row[3]) < MIN:
				O = row[4]
				MIN = int(row[3])
			if int(row[3]) > MAX:
				C = row[4]
				MAX = int(row[3])
			elif int(row[3]) == MAX:
				C = row[4]
				MAX = int(row[3])
			if int(row[4]) > H:
				H = int(row[4])
			if int(row[4]) < L:
				L = int(row[4])
			# row2.append(row)
		else:
			continue
		# if i % 10 == 0:
		# 	print(i)
		
print(O,H,L,C)
# print("stage 2 finished")
# print(row2[0][3]) #84500
# print(4)
# row2 = np.roway(row2)
# print(row2[0])
# print(row2.shape[0])

# for i in range(row2.shape[0]):
# 	if int(row2[i][3]) < MIN:
# 		O = row2[i][4]
# 		MIN = int(row2[i][3])


# for i in range(row2.shape[0]): #從尾巴開始找
# 	if int(row2[i][3]) > MAX:
# 		C = row2[i][4]
# 		MAX = int(row2[i][3])
# 	elif int(row2[i][3]) == MAX:
# 		C = row2[i][4]
# 		MAX = int(row2[i][3])


# H = row2[0][4]
# for i in range(row2.shape[0]):
# 	if row2[i][4] > H:
# 		H = row2[i][4]

# L = row2[0][4]
# for i in range(row2.shape[0]):
# 	if row2[i][4] < L:
# 		L = row2[i][4]
# print(8)
# print(O,H,L,C)