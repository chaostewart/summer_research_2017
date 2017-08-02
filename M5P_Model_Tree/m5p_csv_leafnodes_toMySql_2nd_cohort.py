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

cursor.execute("Drop table if exists chao_draft.m5p_prediction_2nd_cohort;")

mydb.commit()

cursor.execute("""Create table chao_draft.m5p_prediction_2nd_cohort
(id INT, PlayerName VARCHAR(50), DraftAge_norm double, country_group VARCHAR(10), Height_norm double, Weight_norm double, Position VARCHAR(5),
DraftYear INT, Overall INT, CSS_rank_norm double, rs_GP_norm double, rs_G_norm double, rs_A_norm double, rs_P_norm double, rs_PIM_norm double,
rs_PlusMinus_norm double, po_GP_norm double, po_G_norm double, po_A_norm double, po_P_norm double, po_PIM_norm double, po_PlusMinus_norm double,
sum_7yr_GP INT, Predicted_GP DOUBLE, LeafNode INT );""")

mydb.commit()

# where unimported csv files are stored
inputDir = "/home/cla315/work_yeti/m5p_linear_model/test_folder"
# csv files will be moved to hear after being imported to database
moveToDir = "/home/cla315/work_yeti/m5p_linear_model/test_folder"

fileNameList = []
for file in os.listdir(inputDir):
    if file.endswith("2nd_cohort.csv"):
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
			cursor.execute("""INSERT INTO chao_draft.m5p_prediction_2nd_cohort
			(id, PlayerName, DraftAge_norm, country_group, Height_norm, Weight_norm, Position, DraftYear, Overall, CSS_rank_norm,
			rs_GP_norm, rs_G_norm, rs_A_norm, rs_P_norm, rs_PIM_norm, rs_PlusMinus_norm, po_GP_norm, po_G_norm, po_A_norm, po_P_norm,
			po_PIM_norm, po_PlusMinus_norm, sum_7yr_GP, Predicted_GP, LeafNode) VALUES(%s, %s, %s, %s, %s,
			%s, %s, %s, %s, %s,
			%s, %s, %s, %s, %s,
			%s, %s, %s, %s, %s, 
			%s, %s, %s, %s, %s)""", row)
			mydb.commit()
	# now move the imported file to another folder
	shutil.move(inputDir + "/" + fileName, moveToDir + "/" + fileName)

cursor.close()
print "ALL CSV files in folder has been written to database."




