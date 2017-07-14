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
	if file.endswith("class_0.csv"):
		#splitext(file)[0] remove the .txt extension from file name
		fileName = os.path.splitext(file)[0]
		fileNameList.append(fileName)
print fileNameList

lmt_1_weights = [14.888173, -0.594558, -0.064151, 0.984812, -0.060772, -0.051959,
				 -0.013626, 0.201161, -0.275218, -0.354102, 0.117612, 0.071793,
				 0.000708, -0.032364, -0.019283, 0, 0.005115, -0.06627,
				 0.041624, 0, 0.000202, 0.030326, -0.002366, -0.29476]

lmt_2_weights = [23.192864, -0.366244, -0.912607, 1.433599, -0.507366, -0.139773,
				 -0.019528, 0.201161, -0.275218, 0, 0.709981, 0.082468,
				 -0.023495, 0.021848, -0.093936, 0, 0.018377, 0.018502,
				 -0.139301, 0.080361, -0.024596, 0.030326, -0.01143, -0.079145]

lmt_3_weights = [-43.530466, 1.361418, -0.398523, 0.315852, 2.158159, 0.209465,
				 0.04745, -0.836145, 1.610893, -0.30828, 1.63373, 0.002885,
				 -0.009473, -0.06702, 0.117083, 0.002373, -0.009791, -0.071751,
				 -0.000899, -0.006306, -0.868767, -0.16323, -0.080303, 0.024219]

lmt_4_weights = [-0.874123, 0.02324, -0.019999, 1.236313, -0.788247, 0.09399,
				 -0.019981, 0.152174, -0.069806, 0.186689, -0.066931, 0.001568,
				 -0.025475,  0.006235,  -0.021727, 0.002373,  0.001147, -0.010578,
				 -0.018744, -0.006492, -0.015903, 0.03446, -0.010291, 0.040278]

lmt_5_weights = [-4.635535,  -0.097547,  -0.019999,  0.178643, 0.145264,  0.155902,
				 -0.021556, -0.076398,  -0.056732,  0.02793,  -0.230412,  0.005065,
				 -0.028554,  0.008763,  -0.007511,  0.003178, 0.003009,  0.032891,
				 0.008606, -0.03578, -0.002148,  -0.004515, -0.0035,  0.072108]

lmt_6_weights = [2.071775,  0.117162, -0.019999, 1.020877, 0.105905, -0.003321,
				 -0.011691, 0.087315, -0.056732, -0.270935, -0.023859, 0.000709,
				 -0.011266, -0.009656,  -0.007511, 0.00037, 0.002604, -0.006441,
				 0.019336, -0.006492,  -0.043772,  -0.009365, -0.023884, 0.022362]

lmt_7_weights = [-25.903473, -0.219658, -0.017336, 0.300964, -0.060772, 0.666201,
				 -0.087535, 1.033734, -3.000067, 0.01462, -0.059343, 0.002908,
				 -0.047223, -0.018486, -0.010788, 0.001849 , 0.001869, 0.181884,
				 -0.001824, -0.001468, 0.080652, 0, -0.010493, 23.397983]

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
	elif leafNum == '5':
		weights_list = list(lmt_5_weights)
	elif leafNum == '6':
		weights_list = list(lmt_6_weights)
	elif leafNum == '7':
		weights_list = list(lmt_7_weights)
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
				  'CSS_rank': int(row[8]), 'rs_GP':  int(row[9]), 'rs_G': int(row[10]), 'rs_A': int(row[11]), 'rs_P': int(row[12]) ,'rs_PIM': int(row[13]), 'rs_PlusMinus': int(row[14]),
				  'po_GP': int(row[15]), 'po_G': int(row[16]), 'po_A': int(row[17]), 'po_P': int(row[18]), 'po_PIM': int(row[19]), 'po_PlusMinus': int(row[20]) }

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
			xk['sum_7yr_GP'] = row[21]
			xk['GP_greater_than_0'] = row[23]
			xk['sum_wk_xk'] = sum_wk_xk
			xk['class_0_prob'] = class_0_prob
			xk['LeafNode'] = leafNum
			#print str(list(xk.keys()))
			rows_list.append(xk)
		shutil.move(inputDir + "/" + fileName + '.csv', moveToDir + "/" + fileName + '.csv')

	fieldNames = ['id', 'PlayerName', 'DraftAge', 'country_group', 'Height','Weight', 'Position', 'CSS_rank','rs_GP','rs_G', 'rs_A','rs_P', 'rs_PIM',
	'rs_PlusMinus','po_GP','po_G', 'po_A', 'po_P',  'po_PIM', 'po_PlusMinus',  'sum_7yr_GP',   'GP_greater_than_0',
	 'sum_wk_xk', 'class_0_prob', 'LeafNode' ]

		# using the same naming format for csv files
	with open(outputDir + "/leaf_nodes_with_prob.csv", 'wb') as output_file:
		dict_writer = csv.DictWriter(output_file, fieldNames)
		dict_writer.writeheader()
		dict_writer.writerows(rows_list)
	# moved imported .txt file to another  folder


