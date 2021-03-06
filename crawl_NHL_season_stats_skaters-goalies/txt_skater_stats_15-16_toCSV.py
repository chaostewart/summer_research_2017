import csv
import os
import shutil
import time

# newly crawled betting lines are saved in the inputDir folder
#inputDir = "/home/cla315/work_yeti/new_wilson_98_16/seasonstats_txtfiles"
inputDir = "/home/cla315/work_galen/crawl_player_stats_15-16/test_folder"
# csv files to be created will be saved in the outputDir folder
#outputDir = "/home/cla315/work_yeti/new_wilson_98_16/seasonstats_csvfiles"
outputDir = "/home/cla315/work_galen/crawl_player_stats_15-16/test_folder"
# after data is exacted, .txt files will be moved to the moveToDir folder
#moveToDir = "/home/cla315/work_yeti/new_wilson_98_16/seasonstats_oldtxtfiles"
moveToDir = "/home/cla315/work_galen/crawl_player_stats_15-16/test_folder"


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
            ####sample: {'A': '24', 'SHP': '1', 'GWG': '3', 'G': '19', 'GP': '75', 'PlayerName': 'Greg Adams', 'Team': 'PHX', 'P': '43', 'S': '176', 'SHG': '0', 'TOI/GP': '17:22', 'PPG': '5', 'P/GP': '0.57', 'S%': '10.8', 'FOW%': '52.9', '+/-': '-1', 'PIM': '26', 'Position': 'L', 'Season': '1998-99', 'OTG': '0', 'Shifts/GP': '20.9', 'PPP': '11', 'row #': '3'}####
			seasonyr = int(rowDict['Season'][:4])
			rowDict['Season'] = str(seasonyr) + "-" + str(seasonyr + 1)

			nameList = rowDict['PlayerName'].split(' ')
			rowDict['FirstName'] = nameList[0]
			rowDict['LastName'] = nameList[len(nameList) - 1]

			if fileName[-8:] == 'Playoffs':
				rowDict['GameType'] = 'Playoffs'
			else:
				rowDict['GameType'] = 'Regular Season'
			
			dicts_from_file.append(rowDict)
			#print(rowDict)

	# write each line to csv file
	fieldNames = ['PlayerID', 'PlayerName', 'FirstName', 'LastName','Season', 'GameType', 'Team', 'Position', 'GP', 'G', 'A', 'P', '+/-', 'PIM', 'P/GP', 'PPG', 'PPP', 'SHG', 'SHP', 'GWG', 'OTG', 'S', 'S%', 'TOI/GP', 'Shifts/GP', 'FOW%' ]
	# using the same naming format for csv files
	with open(outputDir + "/" + fileName + ".csv", 'wb') as output_file:
		dict_writer = csv.DictWriter(output_file, fieldNames)
		dict_writer.writeheader()
		dict_writer.writerows(dicts_from_file)
	# moved imported .txt file to another  folder
	shutil.move(inputDir + "/" + fileName + ".txt", moveToDir + "/" + fileName + ".txt" )

print "All txt files have been processed."
    
