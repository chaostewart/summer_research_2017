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

cursor.execute("Drop table if exists chao_draft.before_NHL_skaters_stats_1998_2008_original;")

mydb.commit()

cursor.execute("""Create table chao_draft.before_NHL_skaters_stats_1998_2008_original
(PlayerId INT, PlayerName VARCHAR(50), BirthDate DATE, BirthYear INT, BirthMonth INT,
BirthDay INT, Birthplace VARCHAR(70), Country VARCHAR(10), Height_info VARCHAR(10),
Height INT, Weight INT, Position_info VARCHAR(10), Position VARCHAR(5), Shoots VARCHAR(10),
DraftYear INT, DraftRound INT, RoundRank INT, Overall INT, Season VARCHAR(15),
Team VARCHAR(35), GameType VARCHAR(25), GP INT, G INT, A INT, P INT, PlusMinus INT,
PIM  INT, PPG INT, PPP INT, SHG INT, SHP INT, GWG INT, OTG INT,
S INT, ShootingPercentage DOUBLE, FaceoffWinPercentage DOUBLE);""")

mydb.commit()

# where unimported csv files are stored
inputDir = "/home/cla315/work_yeti/new_kurt_98_16/csv_files"
# csv files will be moved to hear after being imported to database
moveToDir = "/home/cla315/work_yeti/new_kurt_98_16/old_csv_files"

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
			cursor.execute("""INSERT INTO chao_draft.before_NHL_skaters_stats_1998_2008_original
			(PlayerId, PlayerName , BirthDate, BirthYear, BirthMonth, BirthDay, Birthplace , Country, Height_info,
Height, Weight, Position_info, Position, Shoots, DraftYear , DraftRound , RoundRank , Overall , Season ,
Team, GameType, GP, G, A, P, PlusMinus, PIM, PPG, PPP, SHG, SHP,
GWG, OTG, S, ShootingPercentage, FaceoffWinPercentage) VALUES(%s, %s, %s, %s, %s, %s, %s, %s,
 %s, %s, %s, %s, %s, %s, %s,
 %s, %s, %s, %s, %s, %s, %s,
 %s, %s, %s, %s, %s, %s, %s,
 %s, %s, %s, %s, %s, %s, %s)""", row)
			mydb.commit()
	# now move the imported file to another folder
	shutil.move(inputDir + "/" + fileName, moveToDir + "/" + fileName)

cursor.close()
print "ALL CSV files in folder has been written to database."




