import csv
import os
import shutil
import time
import numpy as np

# newly crawled betting lines are saved in the inputDir folder
# inputDir = "/home/cla315/work_yeti/LMT_leaf_nodes/leaf_nodes"
inputDir = "/home/cla315/work_yeti/LMT_leaf_nodes/test_folder"
# csv files to be created will be saved in the outputDir folder
#outputDir = "/home/cla315/work_yeti/LMT_leaf_nodes/calculated_data"
outputDir = "/home/cla315/work_yeti/LMT_leaf_nodes/test_folder"
# after data is exacted, .txt files will be moved to the moveToDir folder
#moveToDir = "/home/cla315/work_yeti/LMT_leaf_nodes/old_leaf_nodes"
moveToDir = "/home/cla315/work_yeti/LMT_leaf_nodes/test_folder"

fileNameList = [] # all file names in the input folder are saved in this list
for file in os.listdir(inputDir):
	if file.endswith("2001.csv") or file.endswith("2002.csv"):
		#splitext(file)[0] remove the .txt extension from file name
		fileName = os.path.splitext(file)[0]
		fileNameList.append(fileName)
print fileNameList

"""
'w0': weights_list[0], 'DraftAge': weights_list[1], 'country_CAN':weights_list[2], 'country_EURO':weights_list[3], 'country_USA':weights_list[4], 'Height': weights_list[5], 'Weight': weights_list[6], 'Pos_C':weights_list[7], 'Pos_L': weights_list[8], 'Pos_D': weights_list[9], 'Pos_R': weights_list[10],'CSS_rank':  weights_list[11], 'rs_GP':weights_list[12], 'rs_G': weights_list[13], 'rs_A': weights_list[14], 'rs_P': weights_list[15],'rs_PIM':weights_list[16], 'rs_PlusMinus': weights_list[17],
'po_GP': weights_list[18], 'po_G': weights_list[19],'po_A': weights_list[20], 'po_P':weights_list[21], 'po_PIM': weights_list[22], 'po_PlusMinus': weights_list[23]
"""


lmt_1_weights = [16.41569, -0.15337, 0, 0, -0.155556, 0.016561,
 				-0.01478, 0, -0.198204, 0.044928, 0, 0.008562,
 				-0.004351, 0.001571, -0.003524, -0.001328, 0.00075, 0.006349,
 				0, 0, -0.037136, 0,  -0.004793, 0.026432]

lmt_2_weights = [37.494838, -0.510028, -0.24763, 0.184066, 0.113217, 0.057165, 
				-0.027175, 0, -0.198204, 0.044928, -0.13372, 0.009954, 
				-0.023451,  0.011145, -0.046833,  -0.009815,  -0.020756,  -0.091803, 
				0, -0.053264, 0.002115, 0,  -1.523355, 88.873339]

lmt_3_weights = [2.172986,  -0.16115, -0.305115, 0.184066, 0.209503, 0.11046,  
				-0.033171, 0, -0.198204,  0.044928,  -0.197095,  0.010547, 
				-0.030081,  0.013523, -0.009237,  -0.009815,  0.004605,  -0.25357,
				0, -0.065794,  0.031231, 0, -0.004793, 8.747143]

lmt_4_weights = [21.391429, -0.191226, -0.24763, 2.88254, -0.155556, 0.016561, 
				-0.04876,  -0.554463, -0.198204, 0.044928, 0, -0.016317,
				-0.01418, -0.085525, -0.009237,  -0.003004, 0.002358, -0.021358,
				0, -0.032721, -0.135213, 0, -0.191122, 40.32409]


rows_list = []
for fileName in fileNameList:
	leafNum = fileName[3]
	if leafNum == '1':
		weights_list = list(lmt_1_weights)
	elif leafNum == '2':
		weights_list = list(lmt_2_weights)
	elif leafNum == '3':
		weights_list = list(lmt_3_weights)
	elif leafNum == '4':
		weights_list = list(lmt_4_weights)

	# weights_list = list('lmt_%s_weights' % leafNum)
	print str(weights_list)
	with open(inputDir + "/" + fileName + '.csv','r') as inputFile:
		csv_data = csv.reader(inputFile)
		#the following code avoids importing headers/1st row in each csv file
		firstLine = True
		for row in csv_data:
			if firstLine:
				firstLine = False
				continue
			#print type(row)
			#print row
			class_0_prob = 0
			sum_wk_xk = 0
			wk = {'w0': weights_list[0], 'DraftAge': weights_list[1], 'country_CAN':weights_list[2], 'country_EURO':weights_list[3],
				  'country_USA':weights_list[4],'Height': weights_list[5], 'Weight': weights_list[6], 'Pos_C':weights_list[7], 'Pos_L': weights_list[8],
				  'Pos_D': weights_list[9], 'Pos_R': weights_list[10],'CSS_rank':  weights_list[11], 'rs_GP':weights_list[12], 'rs_G': weights_list[13],
				  'rs_A': weights_list[14], 'rs_P': weights_list[15],'rs_PIM':weights_list[16], 'rs_PlusMinus': weights_list[17],'po_GP': weights_list[18],
				  'po_G': weights_list[19],'po_A': weights_list[20], 'po_P':weights_list[21], 'po_PIM': weights_list[22], 'po_PlusMinus': weights_list[23] }
			xk = {'w0': 1, 'DraftAge': int(row[2]), 'Height': int(row[5]), 'Weight': int(row[6]),
				  'CSS_rank': int(row[9]), 'rs_GP':  int(row[10]), 'rs_G': int(row[11]), 'rs_A': int(row[12]), 'rs_P': int(row[13]) ,'rs_PIM': int(row[14]), 'rs_PlusMinus': int(row[15]),
				  'po_GP': int(row[16]), 'po_G': int(row[17]), 'po_A': int(row[18]), 'po_P': int(row[19]), 'po_PIM': int(row[20]), 'po_PlusMinus': int(row[21]) }

			for key in xk:
				sum_wk_xk = sum_wk_xk + xk[key] * wk[key]
			xk['country_group'] = row[4]
			xk['Position'] = row[7]
			sum_wk_xk = sum_wk_xk + (xk['country_group'] == 'CAN') * wk['country_CAN'] + (xk['country_group'] == 'EURO') * wk['country_EURO'] + (xk['country_group'] == 'USA') * wk['country_USA'] + (xk['Position'] == 'L') * wk['Pos_L'] + (xk['Position'] == 'R') * wk['Pos_R'] + (xk['Position'] == 'C') * wk['Pos_C'] + (xk['Position'] == 'D') * wk['Pos_D']
			#print 'The sum is ' + str(sum_wk_xk)
			class_0_prob = 1/(1 + np.exp(sum_wk_xk))
			#print 'The probability is ' + str(class_0_prob)
			del xk['w0']
			xk['id'] = int(row[0])
			xk['PlayerName'] = row[1]
			xk['sum_7yr_GP'] = row[22]
			xk['GP_greater_than_0'] = row[24]
			xk['sum_wk_xk'] = sum_wk_xk
			xk['class_0_prob'] = class_0_prob
			xk['LeafNode'] = leafNum
			xk['DraftYear'] = int(row[8])
			#print str(list(xk.keys()))
			rows_list.append(xk)
		shutil.move(inputDir + "/" + fileName + '.csv', moveToDir + "/" + fileName + '.csv')

	fieldNames = ['id', 'PlayerName', 'DraftAge', 'country_group', 'Height','Weight', 'Position', 'DraftYear', 'CSS_rank','rs_GP','rs_G', 'rs_A','rs_P', 'rs_PIM',
	'rs_PlusMinus','po_GP','po_G', 'po_A', 'po_P',  'po_PIM', 'po_PlusMinus',  'sum_7yr_GP',   'GP_greater_than_0',
	 'sum_wk_xk', 'class_0_prob', 'LeafNode' ]

		# using the same naming format for csv files
	with open(outputDir + "/first_cohort_2years.csv", 'wb') as output_file:
		dict_writer = csv.DictWriter(output_file, fieldNames)
		dict_writer.writeheader()
		dict_writer.writerows(rows_list)
	# moved imported .txt file to another  folder


