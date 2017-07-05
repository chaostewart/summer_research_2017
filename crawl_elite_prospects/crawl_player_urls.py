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
from selenium.webdriver.support import expected_conditions as EC

# The following crawling script is built on Galen Liu's scripts
# Many thanks to Galen!


# if use linux server
def find_chrome():
	chromedriver = "/home/cla315/chromedriver"
	os.environ["webdriver.chrome.driver"] = chromedriver
	driver = webdriver.Chrome(chromedriver)
	return driver

def jump2search(driver, draftYear):
	print "Now start crawling for draft year = " + str(draftYear)
	year_search_url = "http://www.eliteprospects.com/draft.php?year=" + str(draftYear)
	driver.implicitly_wait(10)
	print "Before driver.get(url)"
	driver.get(year_search_url)
	print "After driver.get(url)"

	return driver

def get_store_directory(draftYr):
	data_directory = "/home/cla315/work_yeti/elite_prospect/url_txt_files/player_urls_" + str(draftYr) + ".txt"
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
	total_num_players_xpath = '/html/body/div[1]/table[3]/tbody/tr/td[5]/p[2]/b'
	total_num_players = driver.find_element_by_xpath(total_num_players_xpath).text
	total_num_players = unicodedata.normalize('NFKD', total_num_players).encode('ascii', 'ignore')
	print "Total number of player drafted in year " + str(draft_year) + " is " + total_num_players

	overall = 1
	# /html/body/div[1]/table[3]/tbody/tr/td[5]/p[2]/table[1]/tbody/tr[5]/td[1]
	row_num = overall + 4

	url_record = []
	while overall < int(total_num_players):
		player_url_dict = {}
		overall_num_xpath = '/html/body/div[1]/table[3]/tbody/tr/td[5]/p[2]/table[1]/tbody/tr[%d]/td[1]' % row_num
		try:
			overall_num = driver.find_element_by_xpath(overall_num_xpath).text
			overall_num = unicodedata.normalize('NFKD', overall_num).encode('ascii', 'ignore')
			overall_num = overall_num[1:]
			print "Overall number being read is " + overall_num
			overall_num = int(overall_num)
			overall = overall_num
		except:
			row_num = row_num + 1
			continue
		player_url_dict = record_dict_value(player_url_dict, 'Overall', overall_num)

		player_url_xpath = '/html/body/div[1]/table[3]/tbody/tr/td[5]/p[2]/table[1]/tbody/tr[%d]/td[3]/a' % row_num
		player_url = driver.find_element_by_xpath(player_url_xpath).get_attribute("href")
		player_url = unicodedata.normalize('NFKD', player_url).encode('ascii', 'ignore')
		print "Player url is " + player_url
		player_url_dict = record_dict_value(player_url_dict, 'PlayerUrl', player_url)

		url_record.append(player_url_dict)
		row_num = row_num + 1

	for url_record_line in url_record:
		txt_file.write(str(url_record_line))
		txt_file.write("\n")

def start_crawl(draftYear):
	chrome_driver = find_chrome()
	driver = jump2search(chrome_driver, draftYear)
	data_directory = get_store_directory(draftYear)
	if os.path.exists(data_directory):
		with open(data_directory, "a") as txt_file:
			crawl_data(txt_file, driver)
	else:
		with open(data_directory, "w") as txt_file:
			crawl_data(txt_file, driver)
	chrome_driver.close()


if __name__ == '__main__':
	for draft_year in range(1998, 2009):
		start_crawl(draft_year)
