import csv
import mysql.connector
import os
import shutil

#connect to database server
mydb = mysql.connector.connect(host='cs-oschulte-01.cs.sfu.ca',
                       user='root',
                       passwd='joinbayes',
                       db='sportlogiq_new')
cursor = mydb.cursor()

# comment the following statements if table has been created
'''
cursor.execute("""Drop table if exists sportlogiq_new.betting_lines;""")

mydb.commit()

cursor.execute("""Create table sportlogiq_new.betting_lines (date DATE, weekday VARCHAR(15), time TIME, timeZone VARCHAR(15), period VARCHAR(20), period_time_remain TIME, 
Away_Team VARCHAR(20), Away_goals INT, Away_betting_line_handicap DOUBLE, Away_betting_line_odds INT, Away_total_line_handicap VARCHAR(20), Away_total_line_odds INT, Away_money_line INT, Home_Team VARCHAR(20), Home_goals INT, Home_betting_line_handicap DOUBLE, Home_betting_line_odds INT, Home_total_line_handicap VARCHAR(20), Home_total_line_odds INT, Home_money_line INT);""")

mydb.commit()
'''
# where unimported csv files are stored
inputDir = "/home/cla315/work_galen/betting_lines_csv" 
# csv files will be moved to hear after being imported to database
moveToDir = "/home/cla315/work_galen/betting_lines_importedToDB"  

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
			cursor.execute("""INSERT INTO betting_lines(date, weekday, time, timeZone, period, period_time_remain, Away_Team, Away_goals, Away_betting_line_handicap, Away_betting_line_odds, Away_total_line_handicap, Away_total_line_odds, Away_money_line, Home_Team, Home_goals, Home_betting_line_handicap, Home_betting_line_odds, Home_total_line_handicap, Home_total_line_odds, Home_money_line ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", row)
			mydb.commit()
	# now move the imported file to another folder
	shutil.move(inputDir + "/" + fileName, moveToDir + "/" + fileName)

cursor.close()
print "ALL CSV files in folder has been imported to database."




