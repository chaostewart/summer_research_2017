import csv
import os
import shutil
import time
import numpy as np

# newly crawled betting lines are saved in the inputDir folder
# inputDir = "/home/cla315/work_yeti/LMT_leaf_nodes/leaf_nodes"
inputDir = "/home/cla315/work_yeti/m5p_linear_model/test_folder"
# csv files to be created will be saved in the outputDir folder
#outputDir = "/home/cla315/work_yeti/LMT_leaf_nodes/calculated_data"
outputDir = "/home/cla315/work_yeti/m5p_linear_model/test_folder"
# after data is exacted, .txt files will be moved to the moveToDir folder
#moveToDir = "/home/cla315/work_yeti/LMT_leaf_nodes/old_leaf_nodes"
moveToDir = "/home/cla315/work_yeti/m5p_linear_model/test_folder"

fileNameList = [] # all file names in the input folder are saved in this list
for file in os.listdir(inputDir):
	if file.endswith("2001_norm.csv") or file.endswith("2002_norm.csv"):
		#splitext(file)[0] remove the .txt extension from file name
		fileName = os.path.splitext(file)[0]
		fileNameList.append(fileName)
print fileNameList

rows_list = []
for fileName in fileNameList:
	with open(inputDir + "/" + fileName + '.csv','r') as inputFile:
		csv_data = csv.reader(inputFile)
		firstLine = True
		for row in csv_data:

			if firstLine:
				firstLine = False
				continue

			CSS_rank = float(row[9])
			rs_A = float(row[12])

			if CSS_rank <= 0.094 and rs_A <= 0.25:
				leafNode = 1
				rs_G = float(row[11])
				rs_PIM = float(row[14])
				po_G = float(row[17])
				po_A = float(row[18])
				Predicted_GP = -379.3755 * CSS_rank - 40.06 * rs_G + 97.7545 * rs_A + 370.327 * rs_PIM - 11.5143 * po_GP + 28.1094 * po_A + 96.4458
			elif CSS_rank <= 0.094 and rs_A > 0.25:
				leafNode = 2
				rs_G = float(row[11])
				po_GP = float(row[16])
				po_A = float(row[18])
				Predicted_GP = -1471.3943*CSS_rank - 33.8006 * rs_G + 82.4804 * rs_A - 11.5143 * po_GP + 28.1094 * po_A + 251.5501
			elif CSS_rank > 0.094:
				leafNode = 3
				DraftAge = float(row[2])
				Height = float(row[4])
				Weight = float(row[5])
				po_GP = float(row[16])
				po_G = float(row[17])
				po_A = float(row[18])
				po_P = float(row[19])
				Predicted_GP = 112.3029 * DraftAge - 139.8669 * Height + 133.5335 * Weight - 12.306 * CSS_rank - 5.112 * po_GP - 207.8328 * po_G + 12.4796 * po_A + 248.4612 * po_P + 87.9381

			'''
			['id',			'PlayerName', 			'DraftAge_norm',			 'country_group',			'Height_norm',
			'Weight_norm',	 'Position',			 'DraftYear',					'Overall',				'CSS_rank_norm',
			'rs_GP_norm', 	'rs_G_norm', 			'rs_A_norm',					'rs_P_norm',			 'rs_PIM_norm',
			'rs_PlusMinus_norm', 'po_GP_norm', 		'po_G_norm', 					'po_A_norm', 				'po_P_norm',
			'po_PIM_norm' , 'po_PlusMinus_norm', 	'sum_7yr_GP']
			'''

			xk = {'id':int(row[0]),'PlayerName': row[1], 'DraftAge_norm': float(row[2]), 'country_group': row[3],'Height_norm': float(row[4]),
				  'Weight_norm': float(row[5]), 'Position': row[6],'DraftYear': int(row[7]),  'Overall':int(row[8]),'CSS_rank_norm': float(row[9]),
				  'rs_GP_norm': float(row[10]), 'rs_G_norm': float(row[11]), 'rs_A_norm': float(row[12]), 'rs_P_norm': float(row[13]), 'rs_PIM_norm': float(row[14]),
				  'rs_PlusMinus_norm': float(row[15]), 'po_GP_norm': float(row[16]), 'po_G_norm': float(row[17]), 'po_A_norm': float(row[18]), 'po_P_norm': float(row[19]),
				  'po_PIM_norm': float(row[20]), 'po_PlusMinus_norm': float(row[21]), 'sum_7yr_GP': int(row[22]), 'Predicted_GP':Predicted_GP, 'LeafNode': leafNode  }
			rows_list.append(xk)
		shutil.move(inputDir + "/" + fileName + '.csv', moveToDir + "/" + fileName + '.csv')

	fieldNames = ['id','PlayerName', 'DraftAge_norm', 'country_group','Height_norm', 'Weight_norm',
				  'Position', 'DraftYear','Overall','CSS_rank_norm', 'rs_GP_norm', 'rs_G_norm', 'rs_A_norm',
				  'rs_P_norm', 'rs_PIM_norm', 'rs_PlusMinus_norm',
				  'po_GP_norm', 'po_G_norm', 'po_A_norm', 'po_P_norm',
				  'po_PIM_norm' , 'po_PlusMinus_norm', 'sum_7yr_GP', 'Predicted_GP', 'LeafNode' ]

		# using the same naming format for csv files
	with open(outputDir + "/m5p_prediction_1st_cohort.csv", 'wb') as output_file:
		dict_writer = csv.DictWriter(output_file, fieldNames)
		dict_writer.writeheader()
		dict_writer.writerows(rows_list)
	# moved imported .txt file to another  folder


