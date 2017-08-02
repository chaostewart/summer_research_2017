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
	if file.endswith("2007_norm.csv") or file.endswith("2008_norm.csv"):
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

			DraftAge = float(row[2])
			Height = float(row[4])
			Weight = float(row[5])
			CSS_rank = float(row[9])
			rs_G = float(row[11])
			rs_A = float(row[12])
			rs_PlusMinus = float(row[15])
			po_GP = float(row[16])
			po_G = float(row[17])
			Position = row[6]

			if CSS_rank <= 0.046:
				leafNode = 1
				rs_G = float(row[11])
				rs_PIM = float(row[14])

				po_A = float(row[18])
				Predicted_GP = 21.0566 * DraftAge - 35.1057 * Height + 41.4793 * Weight - 4378.992 * CSS_rank + 38.0207 * rs_A + 340.4368 * rs_PlusMinus + 128.9131 * po_GP + 32.3314 * po_G + 140.2615
			elif CSS_rank > 0.046:
				leafNode = 2
				rs_G = float(row[11])

				po_A = float(row[18])
				Predicted_GP = 130.9158 * DraftAge - 245.9549 * Height + 166.7878 * Weight - 72.9978 * CSS_rank - 86.6925 * rs_G + 262.1554 * rs_A + 8.0596 * rs_PlusMinus + 156.9023 * po_G + 152.0319
				if Position == 'C' or Position == 'R' or Position == 'L':
					Predicted_GP -= 26.7691
					if Position == 'R' or Position == 'L':
						Predicted_GP += 34.0367

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
	with open(outputDir + "/m5p_prediction_2nd_cohort.csv", 'wb') as output_file:
		dict_writer = csv.DictWriter(output_file, fieldNames)
		dict_writer.writeheader()
		dict_writer.writerows(rows_list)
	# moved imported .txt file to another  folder


