import csv
import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import unicodedata
import time
import os
import sys
import os.path
from selenium.webdriver.support.ui import WebDriverWait

# The following crawling script is built on Galen Liu's scripts
# Many thanks to Galen!


# if use linux server
def find_chrome():
	chromedriver = "/home/cla315/chromedriver"
	os.environ["webdriver.chrome.driver"] = chromedriver
	driver = webdriver.Chrome(chromedriver)
	return driver


def jump2search(driver, playerid):
	print "Now start crawling for PlayerID = " + playerid
	player_search_url = "http://www.nhl.com/player/" + playerid
	driver.get(player_search_url)
	time.sleep(3)
	return driver


def get_store_directory():
	data_directory = "/home/cla315/work_yeti/new_kurt_98_16/txt_files/before_nhl_player_stats_extra.txt"
	return data_directory


def record_dict_value(dict_record, key, value):
	try:
		if value == "":
			dict_record.update({key: "Null"})
		else:
			dict_record.update({key: value})
	except ValueError:
		print "empty value"
		dict_record.update({key: "Null"})
	return dict_record


def crawl_data(txt_file, driver):
	data_record = []

	demographic_dict = {}
	shoots_flag = True
	draft_xpath1 = '//*[@id="summary"]/section[1]/div/div[2]/ul/li[5]'
	draft_xpath2 = '//*[@id="summary"]/section[1]/div/div[2]/ul/li[4]'
	try:
		draft = driver.find_element_by_xpath(draft_xpath1).text
		draft = unicodedata.normalize('NFKD', draft).encode('ascii', 'ignore')
	except:
		draft = driver.find_element_by_xpath(draft_xpath2).text
		draft = unicodedata.normalize('NFKD', draft).encode('ascii', 'ignore')
		# print "Check String" + draft[:5]
		if draft[:5] != "Draft":
			print "No draft info found for player ID = " + playerID
			return
		else:
			shoots_flag = False
			print "No shoot info."

	draft = draft.split(": ")
	try:
		draftList = draft[1].split(', ')
	except IndexError:
		print "is error from here???? " + playerID
		return
	#print draftList
	draftYear = draftList[0][:4]

	print "The year when this player got drafted is " + draftYear
	if int(draftYear) < 1998 or int(draftYear) > 2008:
		print "Draft year is out of range, skip to the next player."
		return

	demographic_dict = record_dict_value(demographic_dict, "DraftYear", draftYear)
	demographic_dict = record_dict_value(demographic_dict, "RoundNumber", draftList[1])
	demographic_dict = record_dict_value(demographic_dict, "DraftNumber", draftList[2])
	# print demographic_dict

	demographic_dict = record_dict_value(demographic_dict, "PlayerId", playerID)

	name_xpath = '//*[@id="summary"]/section[1]/div/div[2]/ul/li[1]/span'
	name = driver.find_element_by_xpath(name_xpath).text
	name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
	demographic_dict = record_dict_value(demographic_dict, "PlayerName", name)

	position_xpath = '//*[@id="content-wrap"]/section[1]/div/section/div[2]/span[1]'
	position = driver.find_element_by_xpath(position_xpath).text
	position = unicodedata.normalize('NFKD', position).encode('ascii', 'ignore')
	demographic_dict = record_dict_value(demographic_dict, "Position", position)

	height_xpath = '//*[@id="content-wrap"]/section[1]/div/section/div[2]/span[2]'
	height = driver.find_element_by_xpath(height_xpath).text
	height = unicodedata.normalize('NFKD', height).encode('ascii', 'ignore')
	# height = height.split(" ")
	# height = height[0]+height[1]
	demographic_dict = record_dict_value(demographic_dict, "Height", height)

	weight_xpath = '//*[@id="content-wrap"]/section[1]/div/section/div[2]/span[3]'
	weight = driver.find_element_by_xpath(weight_xpath).text
	weight = unicodedata.normalize('NFKD', weight).encode('ascii', 'ignore')
	demographic_dict = record_dict_value(demographic_dict, "Weight", weight)

	born_xpath = '//*[@id="summary"]/section[1]/div/div[2]/ul/li[2]'
	born = driver.find_element_by_xpath(born_xpath).text
	born = unicodedata.normalize('NFKD', born).encode('ascii', 'ignore')
	born = born.split(": ")
	demographic_dict = record_dict_value(demographic_dict, "Birthday", born[1])

	birthplace_xpath = '//*[@id="summary"]/section[1]/div/div[2]/ul/li[3]'
	birthplace = driver.find_element_by_xpath(birthplace_xpath).text
	birthplace = unicodedata.normalize('NFKD', birthplace).encode('ascii', 'ignore')
	birthplace = birthplace.split(": ")
	demographic_dict = record_dict_value(demographic_dict, "Birthplace", birthplace[1])

	if shoots_flag:
		shoots_xpath = '//*[@id="summary"]/section[1]/div/div[2]/ul/li[4]'
		shoots = driver.find_element_by_xpath(shoots_xpath).text
		shoots = unicodedata.normalize('NFKD', shoots).encode('ascii', 'ignore')
		shoots = shoots.split(": ")
		demographic_dict = record_dict_value(demographic_dict, "Shoots", shoots[1])
	else:
		demographic_dict = record_dict_value(demographic_dict, "Shoots", "Null")

	driver.find_element_by_xpath('//*[@id="type-career-league"]').click()
	driver.find_element_by_xpath('//*[@id="career"]/ul/li[1]/div/ul/li[1]/a').click()
	time.sleep(3)
	for i in range (1,3):
		driver.find_element_by_xpath('//*[@id="type-career-gametype"]').click()
		gametype_xpath = '//*[@id="career"]/ul/li[2]/div/ul/li[%d]/a' %i
		driver.find_element_by_xpath(gametype_xpath).click()
		time.sleep(3)


		row_num = 1
		flag = True
		while flag:
			data_record_dict = dict(demographic_dict)
			gametype = driver.find_element_by_xpath(gametype_xpath).get_attribute("data-value")
			#gametype = driver.find_element_by_xpath(gametype_xpath).text
			gametype = unicodedata.normalize('NFKD', gametype).encode('ascii', 'ignore')
			print "Game type is " + gametype
			data_record_dict = record_dict_value(data_record_dict, "GameType", gametype)
			table_path = '//*[@id="careerTable"]/div/div/div[1]/div/table/tbody'

			print "Row number is " + str(row_num - 1)
			current_row_path = table_path + "/tr[" + str(row_num) + "]"
			season_xpath = current_row_path + "/td[1]/span"
			try:
				season = driver.find_element_by_xpath(season_xpath).text
			except:
				flag = False
				break
			season = unicodedata.normalize('NFKD', season).encode('ascii', 'ignore')
			print "The season is being read is " + season
			yearList = season.split("-")
			try:
				year = yearList[1]
			except IndexError:
				flag = False
				print "This Player has no playoffs records."
				break
			try:
				int(year)
			except ValueError:
				row_num = row_num + 1
				continue
			if int(year) > int(draftYear):
				flag = False
				break
			elif int(year) < int(draftYear):
				row_num = row_num + 1
				continue
			data_record_dict = record_dict_value(data_record_dict, "Season", season)

			team_xpath = current_row_path + "/td[2]/span"
			team = driver.find_element_by_xpath(team_xpath).text
			team = unicodedata.normalize('NFKD', team).encode('ascii', 'ignore')
			data_record_dict = record_dict_value(data_record_dict, "Team", team)

			gp_xpath = current_row_path + "/td[3]/span"
			gp = driver.find_element_by_xpath(gp_xpath).text
			gp = unicodedata.normalize('NFKD', gp).encode('ascii', 'ignore')
			data_record_dict = record_dict_value(data_record_dict, "GP", gp)

			g_xpath = current_row_path + "/td[4]/span"
			g = driver.find_element_by_xpath(g_xpath).text
			g = unicodedata.normalize('NFKD', g).encode('ascii', 'ignore')
			data_record_dict = record_dict_value(data_record_dict, "G", g)

			a_xpath = current_row_path + "/td[5]/span"
			a = driver.find_element_by_xpath(a_xpath).text
			a = unicodedata.normalize('NFKD', a).encode('ascii', 'ignore')
			data_record_dict = record_dict_value(data_record_dict, "A", a)

			p_xpath = current_row_path + "/td[6]/span"
			p = driver.find_element_by_xpath(p_xpath).text
			p = unicodedata.normalize('NFKD', p).encode('ascii', 'ignore')
			data_record_dict = record_dict_value(data_record_dict, "P", p)

			pm_xpath = current_row_path + "/td[7]/span"
			pm = driver.find_element_by_xpath(pm_xpath).text
			pm = unicodedata.normalize('NFKD', pm).encode('ascii', 'ignore')
			data_record_dict = record_dict_value(data_record_dict, "+/-", pm)

			pim_xpath = current_row_path + "/td[8]/span"
			pim = driver.find_element_by_xpath(pim_xpath).text
			pim = unicodedata.normalize('NFKD', pim).encode('ascii', 'ignore')
			data_record_dict = record_dict_value(data_record_dict, "PIM", pim)

			ppg_xpath = current_row_path + "/td[9]/span"
			ppg = driver.find_element_by_xpath(ppg_xpath).text
			ppg = unicodedata.normalize('NFKD', ppg).encode('ascii', 'ignore')
			data_record_dict = record_dict_value(data_record_dict, "PPG", ppg)

			ppp_xpath = current_row_path + "/td[10]/span"
			ppp = driver.find_element_by_xpath(ppp_xpath).text
			ppp = unicodedata.normalize('NFKD', ppp).encode('ascii', 'ignore')
			data_record_dict = record_dict_value(data_record_dict, "PPP", ppp)

			shg_xpath = current_row_path + "/td[11]/span"
			shg = driver.find_element_by_xpath(shg_xpath).text
			shg = unicodedata.normalize('NFKD', shg).encode('ascii', 'ignore')
			data_record_dict = record_dict_value(data_record_dict, "SHG", shg)

			shp_xpath = current_row_path + "/td[12]/span"
			shp = driver.find_element_by_xpath(shp_xpath).text
			shp = unicodedata.normalize('NFKD', shp).encode('ascii', 'ignore')
			data_record_dict = record_dict_value(data_record_dict, "SHP", shp)

			gwg_xpath = current_row_path + "/td[13]/span"
			gwg = driver.find_element_by_xpath(gwg_xpath).text
			gwg = unicodedata.normalize('NFKD', gwg).encode('ascii', 'ignore')
			data_record_dict = record_dict_value(data_record_dict, "GWG", gwg)

			otg_xpath = current_row_path + "/td[14]/span"
			otg = driver.find_element_by_xpath(otg_xpath).text
			otg = unicodedata.normalize('NFKD', otg).encode('ascii', 'ignore')
			data_record_dict = record_dict_value(data_record_dict, "OTG", otg)

			s_xpath = current_row_path + "/td[15]/span"
			s = driver.find_element_by_xpath(s_xpath).text
			s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
			data_record_dict = record_dict_value(data_record_dict, "S", s)

			spercentage_xpath = current_row_path + "/td[16]/span"
			spercentage = driver.find_element_by_xpath(spercentage_xpath).text
			spercentage = unicodedata.normalize('NFKD', spercentage).encode('ascii', 'ignore')
			data_record_dict = record_dict_value(data_record_dict, "S%", spercentage)

			fow_xpath = current_row_path + "/td[17]/span"
			fow = driver.find_element_by_xpath(fow_xpath).text
			fow = unicodedata.normalize('NFKD', fow).encode('ascii', 'ignore')
			data_record_dict = record_dict_value(data_record_dict, "FOW%", fow)
			print data_record_dict
			data_record.append(data_record_dict)
			row_num = row_num + 1

	for data_record_line in data_record:
		txt_file.write(str(data_record_line))
		txt_file.write("\n")

def start_crawl(playerid):
	chrome_driver = find_chrome()
	search_page_driver = jump2search(chrome_driver, playerid)
	data_directory = get_store_directory()
	if os.path.exists(data_directory):
		with open(data_directory, "a") as txt_file:
			crawl_data(txt_file, search_page_driver)
	else:
		with open(data_directory, "w") as txt_file:
			crawl_data(txt_file, search_page_driver)
	chrome_driver.close()


if __name__ == '__main__':
	with open('/home/cla315/work_yeti/new_kurt_98_16/PlayerID_more.csv', 'r') as inputFile:
		csv_data = csv.reader(inputFile)
		# the following code avoids importing headers/1st row in each csv file
		firstLine = True
		for row in csv_data:
			if firstLine:
				firstLine = False
				continue
			playerID = row[0]
			start_crawl(playerID)
