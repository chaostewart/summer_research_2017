import csv
import os
import shutil
import time

# newly crawled betting lines are saved in the inputDir folder
inputDir = "/home/cla315/work_galen/new_betting_lines"
# csv files to be created will be saved in the outputDir folder
outputDir = "/home/cla315/work_galen/betting_lines_csv"
# after data is exacted, .txt files will be moved to the moveToDir folder
moveToDir = "/home/cla315/work_galen/old_betting_lines"


#Find all .txt files in the inputDir folder
fileNameList = [] # all file names in the input folder are saved in this list
for file in os.listdir(inputDir):
	if file.endswith(".txt"):
		#splitext(file)[0] remove the .txt extension from file name
		fileName = os.path.splitext(file)[0]
		fileNameList.append(fileName)
#print pathList

# Loop through all files
for fileName in fileNameList:
	dicts_from_file = []
	with open(inputDir + "/" + fileName + ".txt",'r') as betting_lines:
		# lastList saves the last betting line that has been imported to csv file
		lastList=[] 
		for line in betting_lines:
			rowDict = eval(line) 
			#convert one string line to a python dictionary
            '''sample: {'Away_betting_line_handicap': '+1.5', 'Home_goals': '0', 'Away_Team': 'OTT Senators', 'Away_total_line_odds': '-140', 'Away_goals': '0', 'Home_total_line_handicap': 'U 3.5', 'Home_betting_line_handicap': '-1.5', 'Home_Team': 'PIT Penguins', 'Home_money_line': '-220', 'Home_betting_line_odds': '+180', 'Away_total_line_handicap': 'O 3.5', 'period_time_remain': '02:42', 'Away_money_line': '+175', 'period': 'P1', 'time': '17:42:43 PT, Mon May 15 2017', 'Home_total_line_odds': '+110', 'Away_betting_line_odds': '-225'}'''
			strToSplit = rowDict.get("time") # e.g. '17:42:43 PT, Mon May 15 2017'
			strList = strToSplit.split(", ") # e.g. ['17:42:43 PT', 'Mon May 15 2017']
			#print strList
			timeStr = strList[0]
			dateStr = strList[1]  # e.g. 'Mon May 15 2017'
			timeList = timeStr.split(" ") # e.g. ['17:42:43', 'PT']
			rowDict["time"] = timeList[0]
			rowDict["timeZone"] = timeList[1]
			parseDate = time.strptime(dateStr, '%a %b %d %Y')
            # e.g. time.struct_time(tm_year=2017, tm_mon=5, tm_mday=15, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=4, tm_yday=135, tm_isdst=-1)
			rowDict["date"] = time.strftime('%Y-%m-%d', parseDate)  # e.g. '2017-05-15'
			rowDict["weekday"] = time.strftime('%a', parseDate)	 # e.g. 'Mon'
			list = (rowDict).values()
			#print(rowDict)
						
			#the following is to delete duplicated betting lines
			#indices of multiple items to be removed from list
			indices = 2, 3, 8, 12, 14, 15, 16, 17
			list = [i for j, i in enumerate(list) if j not in indices]

			if list == lastList:
				continue
			else:
				dicts_from_file.append(rowDict)
				lastList = list

	# write each line to csv file
	fieldNames = ['date', 'weekday', 'time', 'timeZone', 'period', 'period_time_remain',      'Away_Team', 'Away_goals', 'Away_betting_line_handicap', 'Away_betting_line_odds', 'Away_total_line_handicap', 'Away_total_line_odds', 'Away_money_line',
                      'Home_Team', 'Home_goals', 'Home_betting_line_handicap',
                      'Home_betting_line_odds', 'Home_total_line_handicap',
                      'Home_total_line_odds', 'Home_money_line' ]
	# using the same naming format for csv files
	with open(outputDir + "/" + fileName + ".csv", 'wb') as output_file:
		dict_writer = csv.DictWriter(output_file, fieldNames)
		dict_writer.writeheader()
		dict_writer.writerows(dicts_from_file)
	# moved imported .txt file to another  folder
	shutil.move(inputDir + "/" + fileName + ".txt", moveToDir + "/" + fileName + ".txt" )

    
