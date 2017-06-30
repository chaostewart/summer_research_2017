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

cursor.execute("Drop table if exists chao_draft.NHL_CompleteSkaterStats_1998_2016;")

mydb.commit()

cursor.execute("""Create table chao_draft.NHL_CompleteSkaterStats_1998_2016 (PlayerID INT, PlayerName VARCHAR(50), Season VARCHAR(15), SeasonType VARCHAR(20), Team VARCHAR(35), Position VARCHAR(10), GP INT, G INT, A INT, P INT, PlusMinus INT, PIM  INT, PointPerGame DOUBLE, PPG INT, PPP INT, SHG INT, SHP INT, GWG INT, OTG INT, S INT, ShootingPercentage DOUBLE, TOIPerGame TIME, TOIPerGame_sec INT, ShiftsPerGame DOUBLE, FaceoffWinPercentage DOUBLE);""")

mydb.commit()

# where unimported csv files are stored
inputDir = "/home/cla315/work_yeti/NHL_player_stats_season_by_season_csv_files"
# csv files will be moved to hear after being imported to database
moveToDir = "/home/cla315/work_yeti/processed_NHL_player_stats_season_by_season_csv_files"

fileNameList = []
for file in os.listdir(inputDir):
    if file.endswith(".csv"):
		fileNameList.append(file)	
print "THe following csv files will be imported to the database."
print(fileNameList)		


for fileName in fileNameList:
	with open(inputDir + "/" + fileName,'r')  as inputFile:
		csv_data = csv.reader(inputFile)
		#the following code avoids importing headers/1st row in each csv file
		firstLine = True
		for row in csv_data:
			if firstLine:
				firstLine = False
				continue
			cursor.execute("""INSERT INTO chao_draft.NHL_CompleteSkaterStats_1998_2016 (PlayerID, PlayerName, Season, SeasonType, Team, Position, GP, G, A, P, PlusMinus, PIM, PointPerGame, PPG, PPP, SHG, SHP, GWG, OTG, S, ShootingPercentage, TOIPerGame, TOIPerGame_sec, ShiftsPerGame, FaceoffWinPercentage) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", row)
			mydb.commit()
	# now move the imported file to another folder
	shutil.move(inputDir + "/" + fileName, moveToDir + "/" + fileName)

cursor.close()
print "ALL CSV files in folder has been written to database."



