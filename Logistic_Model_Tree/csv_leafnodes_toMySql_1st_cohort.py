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

cursor.execute("Drop table if exists chao_draft.prediction_1st_cohort;")

mydb.commit()

cursor.execute("""Create table chao_draft.prediction_1st_cohort
(id INT, PlayerName VARCHAR(50), DraftAge INT, country_group VARCHAR(10), Height INT, Weight INT, Position VARCHAR(5), DraftYear INT, CSS_rank INT, rs_GP INT, rs_G INT, rs_A INT, rs_P INT, rs_PIM INT, rs_PlusMinus INT, po_GP INT, po_G INT, po_A INT, po_P INT, po_PIM INT, po_PlusMinus INT, sum_7yr_GP INT, GP_greater_than_0 VARCHAR(10), sum_wk_xk DOUBLE, class_0_prob DOUBLE, LeafNode INT );""")

mydb.commit()

# where unimported csv files are stored
inputDir = "/home/cla315/work_yeti/LMT_leaf_nodes/test_folder"
# csv files will be moved to hear after being imported to database
moveToDir = "/home/cla315/work_yeti/LMT_leaf_nodes/test_folder"

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
			cursor.execute("""INSERT INTO chao_draft.prediction_1st_cohort
			(id, PlayerName, DraftAge, country_group, Height, Weight, Position, DraftYear, CSS_rank, rs_GP, rs_G, rs_A, rs_P, rs_PIM, rs_PlusMinus, po_GP, po_G, po_A, po_P, po_PIM, po_PlusMinus, sum_7yr_GP, GP_greater_than_0, sum_wk_xk, class_0_prob, LeafNode) VALUES(%s, %s, %s, %s, %s,
			%s, %s, %s, %s, %s, %s,
			%s, %s,%s, %s, %s, 
			%s, %s, %s, %s, %s, 
			%s, %s, %s, %s, %s)""", row)
			mydb.commit()
	# now move the imported file to another folder
	shutil.move(inputDir + "/" + fileName, moveToDir + "/" + fileName)

cursor.close()
print "ALL CSV files in folder has been written to database."




