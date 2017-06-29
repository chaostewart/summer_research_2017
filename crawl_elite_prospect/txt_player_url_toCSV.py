import csv
import os
import shutil
import time

# newly crawled betting lines are saved in the inputDir folder
inputDir = "/home/cla315/work_yeti/elite_prospect/url_txt_files"
#inputDir = "/home/cla315/work_yeti/test_folder"
# csv files to be created will be saved in the outputDir folder
outputDir = "/home/cla315/work_yeti/elite_prospect/url_csv_files"
#outputDir = "/home/cla315/work_yeti/test_folder"
# after data is exacted, .txt files will be moved to the moveToDir folder
moveToDir = "/home/cla315/work_yeti/elite_prospect/url_txt_files"
#moveToDir = "/home/cla315/work_yeti/test_folder"


#Find all .txt files in the inputDir folder
fileNameList = []
# all file names in the input folder are saved in this list
for file in os.listdir(inputDir):
	if file.endswith(".txt"):
		# splitext(file)[0] remove the .txt extension from file name
		fileName = os.path.splitext(file)[0]
		fileNameList.append(fileName)
print fileNameList

# Loop through all files
for fileName in fileNameList:
	dicts_from_file = []
	with open(inputDir + "/" + fileName + ".txt",'r') as betting_lines:
		# lastList saves the last betting line that has been imported to csv file
		lastList = []
		for line in betting_lines:
			rowDict = eval(line)

			# convert one string line to a python dictionary
			# {'PlayerUrl': 'http://www.eliteprospects.com/player.php?player=8657', 'Overall': 10}
			dicts_from_file.append(rowDict)
	# write each line to csv file
	fieldNames = ['Overall', 'PlayerUrl']
	# using the same naming format for csv files
	with open(outputDir + "/" + fileName + ".csv", 'wb') as output_file:
		dict_writer = csv.DictWriter(output_file, fieldNames)
		dict_writer.writeheader()
		dict_writer.writerows(dicts_from_file)
	# moved imported .txt file to another  folder
	shutil.move(inputDir + "/" + fileName + ".txt", moveToDir + "/" + fileName + ".txt" )

print "All txt files have been processed."
