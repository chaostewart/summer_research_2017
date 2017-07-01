import csv
import os
import shutil
import time

# newly crawled betting lines are saved in the inputDir folder
inputDir = "/home/cla315/work_yeti/new_kurt_98_16/txt_files"
#inputDir = "/home/cla315/work_yeti/test_folder"
# csv files to be created will be saved in the outputDir folder
outputDir = "/home/cla315/work_yeti/new_kurt_98_16/csv_files"
#outputDir = "/home/cla315/work_yeti/test_folder"
# after data is exacted, .txt files will be moved to the moveToDir folder
moveToDir = "/home/cla315/work_yeti/new_kurt_98_16/old_txt_files"
#moveToDir = "/home/cla315/work_yeti/test_folder"


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

			#  {'PlayerId': '8469770','PlayerName': 'Dennis Wideman','Birthday': 'March 20, 1983',
			#  'Birthplace': 'Kitchener, ON, CAN','Height': '6\' 0"', 'Weight': '202 lb','Position': 'D',
			#  'Shoots': 'Right','DraftYear': '2002', 'RoundNumber': '8th rd', 'DraftNumber': '12th pk (241st overall)',
			# 'Season': '2001-2002','Team': 'London Knights','GameType': 'P', 'GP': '12','G': '4', 'A': '9',
			#  'P': '13','+/-': '--', 'PIM': '26','PPG': '--','PPP': '--', 'SHG': '--', 'SHP': '--',
			#  'GWG': '--', 'OTG': '--',  'S': '--','S%': '--', 'FOW%': '0'}
			dateStr = rowDict['Birthday']
			del rowDict['Birthday']
			parseDate = time.strptime(dateStr, '%B %d, %Y')
			# e.g. time.struct_time(tm_year=2017, tm_mon=5, tm_mday=15, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=4, tm_yday=135, tm_isdst=-1)
			rowDict['BirthDate'] = time.strftime('%Y-%m-%d', parseDate)  # e.g. '2017-05-15'
			rowDict['BirthYear'] = time.strftime('%Y', parseDate)
			rowDict['BirthMonth'] = time.strftime('%m', parseDate)
			rowDict['BirthDay'] = time.strftime('%d', parseDate)

			placeList = rowDict['Birthplace'].split(', ')
			rowDict['Country'] = placeList[len(placeList) - 1]

			rowDict['Position_info'] = rowDict['Position']
			rowDict['Position'] = rowDict['Position'][:1]

			heightList = rowDict['Height'].split("\'")
			foot = int(heightList[0])
			inch = int(heightList[1][:-1])
			rowDict['Height_info'] = rowDict['Height']
			rowDict['Height'] = foot * 12 + inch

			weightList = rowDict['Weight'].split(' ')
			rowDict['Weight'] = weightList[0]

			rowDict['DraftRound'] = rowDict['RoundNumber'][:-5]
			del rowDict['RoundNumber']

			overallList = rowDict['DraftNumber'].split(' (')
			rowDict['RoundRank'] = overallList[0][:-5]
			rowDict['Overall'] = overallList[1][:-11]
			del rowDict['DraftNumber']

			rowDict['PlusMinus'] = rowDict['+/-']
			del rowDict['+/-']

			if rowDict['GameType'] == "P":
				rowDict['GameType'] = "Playoffs"
			elif rowDict['GameType'] == "R":
				rowDict['GameType'] = "Regular Season"

			dicts_from_file.append(rowDict)
			print(rowDict)

	# write each line to csv file
	fieldNames = ['PlayerId', 'PlayerName', 'BirthDate', 'BirthYear', 'BirthMonth', 'BirthDay', 'Birthplace', 'Country',
				  'Height_info', 'Height', 'Weight','Position_info', 'Position', 'Shoots', 'DraftYear','DraftRound', 'RoundRank','Overall','Season',
				  'Team','GameType', 'GP', 'G', 'A', 'P', 'PlusMinus', 'PIM', 'PPG', 'PPP', 'SHG', 'SHP', 'GWG', 'OTG', 'S', 'S%', 'FOW%' ]

	#  'Shoots': 'Right','DraftYear': '2002', 'RoundNumber': '8th rd', 'DraftNumber': '12th pk (241st overall)',
	# 'Season': '2001-2002','Team': 'London Knights','GameType': 'P', 'GP': '12','G': '4', 'A': '9',
	#  'P': '13','+/-': '--', 'PIM': '26','PPG': '--','PPP': '--', 'SHG': '--', 'SHP': '--',
	#  'GWG': '--', 'OTG': '--',  'S': '--','S%': '--', 'FOW%': '0'}

	# using the same naming format for csv files
	with open(outputDir + "/" + fileName + ".csv", 'wb') as output_file:
		dict_writer = csv.DictWriter(output_file, fieldNames)
		dict_writer.writeheader()
		dict_writer.writerows(dicts_from_file)
	# moved imported .txt file to another  folder
	shutil.move(inputDir + "/" + fileName + ".txt", moveToDir + "/" + fileName + ".txt" )

print "All txt files have been processed."
    
