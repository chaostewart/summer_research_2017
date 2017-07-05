import csv
import os
import shutil
import time

# newly crawled betting lines are saved in the inputDir folder
inputDir = "/home/cla315/work_yeti/elite_prospect/playerstats_txtfiles"
# inputDir = "/home/cla315/work_yeti/elite_prospect/test_folder"
# csv files to be created will be saved in the outputDir folder
outputDir = "/home/cla315/work_yeti/elite_prospect/playerstats_csvfiles"
# outputDir = "/home/cla315/work_yeti/elite_prospect/test_folder"
# after data is exacted, .txt files will be moved to the moveToDir folder
moveToDir = "/home/cla315/work_yeti/elite_prospect/playerstats_oldtxtfiles"
# moveToDir = "/home/cla315/work_yeti/elite_prospect/test_folder"


#Find all .txt files in the inputDir folder
fileNameList = [] # all file names in the input folder are saved in this list
for file in os.listdir(inputDir):
	if file.endswith(".txt"):
		#splitext(file)[0] remove the .txt extension from file name
		fileName = os.path.splitext(file)[0]
		fileNameList.append(fileName)
print fileNameList

# Loop through all files
for fileName in fileNameList:
	dicts_from_file = []
	with open(inputDir + "/" + fileName + ".txt",'r') as betting_lines:
		# lastList saves the last betting line that has been imported to csv file
		lastList=[]
		for line in betting_lines:
			rowDict = eval(line)
			#convert one string line to a python dictionary
			demographic_dict = {}
			demographic_dict['eliteId'] = rowDict['eliteId']
			demographic_dict['PlayerName'] = rowDict['PlayerName'].title()

			dateStr = rowDict['BirthDate']
			dateList = dateStr.split('-')
			demographic_dict['BirthYear'] = dateList[0]
			demographic_dict['BirthMonth'] = dateList[1]
			demographic_dict['BirthDay'] = dateList[2]
			demographic_dict['BirthDate'] = rowDict['BirthDate']

			demographic_dict['Birthplace'] = rowDict['Birthplace']
			demographic_dict['Nation'] = rowDict['Nation']

			demographic_dict['Position_info'] = rowDict['Position']
			demographic_dict['Position'] = demographic_dict['Position_info'][:1]

			demographic_dict['Shoots'] = rowDict['Shoots']

			heightList = rowDict['Height'].split(' / ')
			heightList = heightList[1].split('\'')
			foot = int(heightList[0])
			inch = int(heightList[1][:-1])
			demographic_dict['Height'] = foot * 12 + inch
			demographic_dict['Height_info'] = rowDict['Height']

			weightList = rowDict['Weight'].split(' / ')
			weightList = weightList[1].split(' ')
			demographic_dict['Weight'] = weightList[0]
			demographic_dict['Weight_info'] = rowDict['Weight']

			demographic_dict['DraftYear'] = rowDict['draftYear']
			demographic_dict['DraftRound'] = rowDict['draftRound']
			demographic_dict['Overall'] = rowDict['Overall']
			demographic_dict['OverallBy'] = rowDict['overallBy']

			seasonyr = rowDict['Season'].split("-")
			seasonyr = int(seasonyr[0])
			demographic_dict['Season'] = str(seasonyr) + '-' + str(seasonyr+1)
			demographic_dict['Team'] = rowDict['Team']
			demographic_dict['League'] = rowDict['League']

			gametype_dict = {'Reg_':'Regular Season', 'Play_':'Playoffs'}
			prefix_list = ['Reg_']
			if rowDict['Post'] == 'Playoffs':
				prefix_list.append('Play_')
			for prefix in prefix_list:
				data_record_dict = dict(demographic_dict)
				data_record_dict['GameType'] = gametype_dict['%s' % prefix]
				data_record_dict['GP'] = rowDict['%sGP' % prefix]
				data_record_dict['G'] = rowDict['%sG' % prefix]
				data_record_dict['A'] = rowDict['%sA' % prefix]
				data_record_dict['P'] = rowDict['%sTP' % prefix]
				data_record_dict['PIM'] = rowDict['%sPIM' % prefix]
				data_record_dict['PlusMinus'] = rowDict['%sPlusMinus' % prefix]
				dicts_from_file.append(data_record_dict)
				print(data_record_dict)

	# write each line to csv file
	fieldNames = ['eliteId', 'PlayerName', 'BirthDate', 'BirthYear', 'BirthMonth', 'BirthDay', 'Birthplace', 'Nation',
				   'Height_info','Height', 'Weight_info','Weight','Position_info', 'Position', 'Shoots', 'DraftYear','DraftRound','Overall','OverallBy','Season',
				  'Team', 'League','GameType', 'GP', 'G', 'A', 'P',  'PIM','PlusMinus' ]

	# using the same naming format for csv files
	with open(outputDir + "/" + fileName + ".csv", 'wb') as output_file:
		dict_writer = csv.DictWriter(output_file, fieldNames)
		dict_writer.writeheader()
		dict_writer.writerows(dicts_from_file)
	# moved imported .txt file to another  folder
	shutil.move(inputDir + "/" + fileName + ".txt", moveToDir + "/" + fileName + ".txt" )

print "All txt files have been processed."

