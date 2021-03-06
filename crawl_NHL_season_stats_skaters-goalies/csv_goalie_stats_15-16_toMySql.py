import csv
import mysql.connector
import os
import shutil

#connect to database server
mydb = mysql.connector.connect(host='cs-oschulte-01.cs.sfu.ca',
                       user='root',
                       passwd='joinbayes',
                       db='chao_draft')
cursor = mydb.cursor()

# comment the following statements if table has been created

cursor.execute("Drop table if exists chao_draft.galen_goalie_stats_2015_2016_original;")

mydb.commit()

cursor.execute("""Create table chao_draft.galen_goalie_stats_2015_2016_original (PlayerID INT, PlayerName VARCHAR(50), FirstName VARCHAR(50), LastName VARCHAR(50), Season VARCHAR(15), GameType VARCHAR(20), Team VARCHAR(35), Position VARCHAR(10), GP INT, GS INT, W INT, L INT, T INT, OT INT, SA INT, Svs INT, GA INT, SvPercentage DOUBLE, GAA DOUBLE, TOI VARCHAR(10), SO INT, G INT, A INT, P INT, PIM INT);""")

mydb.commit()

# where unimported csv files are stored
inputDir = "/home/cla315/work_galen/crawl_player_stats_15-16/test_folder/old_goalies"
# csv files will be moved to hear after being imported to database
moveToDir = "/home/cla315/work_galen/crawl_player_stats_15-16/test_folder/old_goalies"

fileNameList = []
for file in os.listdir(inputDir):
    if file.endswith(".csv"):
		fileNameList.append(file)	
print "THe following csv files will be imported to the database."
print(fileNameList)		


for fileName in fileNameList:
	with open(inputDir + "/" + fileName,'r') as inputFile:
		csv_data = csv.reader(inputFile)
		#the following code avoids importing headers/1st row in each csv file
		firstLine = True
		for row in csv_data:
			if firstLine:
				firstLine = False
				continue
			cursor.execute("""INSERT INTO chao_draft.galen_goalie_stats_2015_2016_original (PlayerID, PlayerName, FirstName, LastName, Season, GameType, Team, Position, GP, GS, W, L, T, OT, SA, Svs, GA, SvPercentage, GAA, TOI, SO, G, A, P, PIM) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,    %s, %s, %s, %s, %s)""", row)
			mydb.commit()
	# now move the imported file to another folder
	shutil.move(inputDir + "/" + fileName, moveToDir + "/" + fileName)

cursor.close()
print "ALL CSV files in folder has been written to database."




