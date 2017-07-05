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

cursor.execute("Drop table if exists chao_draft.elite_prospects_skaters_stats_1998_2008_original;")

mydb.commit()

cursor.execute("""Create table chao_draft.elite_prospects_skaters_stats_1998_2008_original
(eliteId INT, PlayerName VARCHAR(50), BirthDate DATE, BirthYear INT, BirthMonth INT,
BirthDay INT, Birthplace VARCHAR(70), Nation VARCHAR(10), Height_info VARCHAR(20),
Height INT, Weight_info VARCHAR(35), Weight INT, Position_info VARCHAR(10), Position VARCHAR(5), Shoots VARCHAR(10),
DraftYear INT, DraftRound INT, Overall INT,OverallBy VARCHAR(35),Season VARCHAR(15),
Team VARCHAR(35), League VARCHAR(25), GameType VARCHAR(25), GP INT, G INT, A INT, P INT, PIM INT, PlusMinus INT);""")

mydb.commit()

# where unimported csv files are stored
inputDir = "/home/cla315/work_yeti/elite_prospect/playerstats_csvfiles"
# csv files will be moved to hear after being imported to database
moveToDir = "/home/cla315/work_yeti/elite_prospect/playerstats_oldcsvfiles"

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
			cursor.execute("""INSERT INTO chao_draft.elite_prospects_skaters_stats_1998_2008_original
			(eliteId, PlayerName, BirthDate, BirthYear, BirthMonth, BirthDay, Birthplace, Nation, Height_info,
Height, Weight_info, Weight, Position_info, Position, Shoots, DraftYear, DraftRound, Overall, OverallBy, Season,
Team, League, GameType, GP, G, A, P, PIM, PlusMinus) VALUES(%s, %s, %s, %s, %s, %s,
 %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", row)
			mydb.commit()
	# now move the imported file to another folder
	shutil.move(inputDir + "/" + fileName, moveToDir + "/" + fileName)

cursor.close()
print "ALL CSV files in folder has been written to database."




