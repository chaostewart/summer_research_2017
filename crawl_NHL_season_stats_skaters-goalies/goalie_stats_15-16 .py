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

# The following crawling script is built on Galen Liu's scripts
# Many thanks to Galen!


# if use linux server
def find_chrome():
    chromedriver = "/home/cla315/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    return driver


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


def jump2search(driver, gametype, season):
	if gametype == 2:
		gametype_str = "Regular Season"
	elif gametype == 3:
		gametype_str = "Playoffs"
	print "Now start crawling for Season " + str(season) + "-" + str(season + 1) + " " + gametype_str
	season_str = str(season)+str(season+1)
	player_search_url = "http://www.nhl.com/stats/player?aggregate=0&gameType=" + str(gametype) + "&report=goaliesummary&pos=G&reportType=season&seasonFrom=" + season_str + "&seasonTo=" + season_str + "&filter=gamesPlayed,gte,0&sort=playerName"
	driver.get(player_search_url)
	time.sleep(3)
	return driver


def get_store_directory(season, gametype):
	gametype_str=""
	if gametype == 2:
		gametype_str = "RegularSeason"
	elif gametype == 3:
		gametype_str = "Playoffs"
		
	data_directory = "/home/cla315/work_galen/crawl_player_stats_15-16/goalie_" + str(season) +"_" + str(season+1) + "_" + gametype_str + ".txt"
	return data_directory


def crawl_data(txt_file, driver):

	# //*[@id="stats-page-body"]/div[3]/div[2]/div/div[2]/span[2]/span
	try:
		num_pages_text =driver.find_element_by_xpath('//*[@id="stats-page-body"]/div[3]/div[2]/div/div[2]/span[2]/span').text
		num_pages_text = unicodedata.normalize('NFKD', num_pages_text).encode('ascii', 'ignore')
		#str2_list = num_pages_text.split(" ")
		total_num_pages = int(num_pages_text)
		print "Total number of pages to be crawled is " + str(total_num_pages)
	except:
		print 'only one page of players.'
		total_num_pages = 1
	lastPage = True
	print 'check point 1'
	for page_num in range(0, total_num_pages):
		print 'check point 2'
	#go to that page
		data_record = []
		if lastPage:
			lastPage = False
		else:
			page_pointer = driver.find_element_by_xpath('//*[@id="stats-page-body"]/div[3]/div[2]/div/div[1]/button').click()
		# //*[@id="stats-page-body"]/div[3]/div[2]/div/div[2]/span[2]/div/input
		try:
			curr_page_num = driver.find_element_by_xpath(
				'//*[@id="stats-page-body"]/div[3]/div[2]/div/div[2]/span[2]/div/input').get_attribute("value")
			curr_page_num = unicodedata.normalize('NFKD', curr_page_num).encode('ascii', 'ignore')
			print "Currently crawling page # " + curr_page_num
		except:
			print 'only one page, cannot turn pages.'
		total_num_rows = len(driver.find_elements_by_class_name('rt-tr-group'))
		print "Total number of rows is " + str(total_num_rows)         # including blank rows

		row_path = '//*[@id="stats-page-body"]/div[3]/div[1]/div[3]'
		for row_num in range(1, total_num_rows + 1):
			data_record_dict = {}
			# //*[@id="stats-page-body"]/div[3]/div[1]/div[3]/div[1]
			current_row_path = row_path + "/div[" + str(row_num) + "]"

			try:
				# //*[@id="stats-page-body"]/div[3]/div[1]/div[3]/div[1]/div/div[2]/div/a
				id_url_xpath = current_row_path + "/div/div[2]/div/a"
				id_url = driver.find_element_by_xpath(id_url_xpath).get_attribute("href")
			except:
				print "row number is " + str(row_num)
				break

			id_url = unicodedata.normalize('NFKD', id_url).encode('ascii', 'ignore')
			player_id = id_url[(len(id_url)-7):]
			print "player id is " + player_id
			data_record_dict = record_dict_value(data_record_dict, "PlayerID", player_id)

			# //*[@id="stats-page-body"]/div[3]/div[1]/div[3]/div[1]/div/div[2]/div/a
			player_name_xpath = current_row_path + "/div/div[2]/div/a"
			player_name = driver.find_element_by_xpath(player_name_xpath).text
			player_name = unicodedata.normalize('NFKD', player_name).encode('ascii', 'ignore')
			data_record_dict = record_dict_value(data_record_dict, "PlayerName", player_name)

			# //*[@id="stats-page-body"]/div[3]/div[1]/div[3]/div[1]/div/div[3]/div
			season_xpath =  current_row_path + "/div/div[3]/div"
			season = driver.find_element_by_xpath(season_xpath).text
			season = unicodedata.normalize('NFKD', season).encode('ascii', 'ignore')
			data_record_dict =  record_dict_value(data_record_dict, "Season", season)

			# //*[@id="stats-page-body"]/div[3]/div[1]/div[3]/div[1]/div/div[4]
			team_xpath = current_row_path + "/div/div[4]"
			team = driver.find_element_by_xpath(team_xpath).text
			team = unicodedata.normalize('NFKD', team).encode('ascii', 'ignore')
			data_record_dict = record_dict_value(data_record_dict, "Team", team)

			# //*[@id="stats-page-body"]/div[3]/div[1]/div[3]/div[1]/div/div[5]
			pos_xpath = current_row_path + "/div/div[5]"
			pos = driver.find_element_by_xpath(pos_xpath).text
			pos = unicodedata.normalize('NFKD', pos).encode('ascii', 'ignore')
			data_record_dict = record_dict_value(data_record_dict, "Position", pos)

			# //*[@id="stats-page-body"]/div[3]/div[1]/div[3]/div[1]/div/div[6]
			gp_xpath = current_row_path + "/div/div[6]"
			gp = driver.find_element_by_xpath(gp_xpath).text
			gp = unicodedata.normalize('NFKD', gp).encode('ascii', 'ignore')
			data_record_dict = record_dict_value(data_record_dict, "GP", gp)

			# //*[@id="stats-page-body"]/div[3]/div[1]/div[3]/div[1]/div/div[7]
			gs_xpath =  current_row_path + "/div/div[7]"
			gs = driver.find_element_by_xpath(gs_xpath).text
			gs = unicodedata.normalize('NFKD', gs).encode('ascii', 'ignore')
			data_record_dict = record_dict_value(data_record_dict, "GS", gs)

			# //*[@id="stats-page-body"]/div[3]/div[1]/div[3]/div[1]/div/div[8]
			w_xpath = current_row_path + "/div/div[8]"
			w = driver.find_element_by_xpath(w_xpath).text
			w = unicodedata.normalize('NFKD', w).encode('ascii', 'ignore')
			data_record_dict = record_dict_value(data_record_dict, "W", w)

			# //*[@id="stats-page-body"]/div[3]/div[1]/div[3]/div[1]/div/div[9]
			l_xpath = current_row_path + "/div/div[9]"
			l = driver.find_element_by_xpath(l_xpath).text
			l = unicodedata.normalize('NFKD', l).encode('ascii', 'ignore')
			data_record_dict = record_dict_value(data_record_dict, "L", l)

			# //*[@id="stats-page-body"]/div[3]/div[1]/div[3]/div[1]/div/div[10]
			t_xpath = current_row_path + "/div/div[10]"
			t = driver.find_element_by_xpath(t_xpath).text
			t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore')
			data_record_dict = record_dict_value(data_record_dict, "T", t)

			# //*[@id="stats-page-body"]/div[3]/div[1]/div[3]/div[1]/div/div[11]
			ot_xpath = current_row_path + "/div/div[11]"
			ot = driver.find_element_by_xpath(ot_xpath).text
			ot = unicodedata.normalize('NFKD', ot).encode('ascii', 'ignore')
			data_record_dict = record_dict_value(data_record_dict, "OT", ot)

			# //*[@id="stats-page-body"]/div[3]/div[1]/div[3]/div[1]/div/div[12]/div
			sa_xpath = current_row_path + "/div/div[12]"
			sa = driver.find_element_by_xpath(sa_xpath).text
			sa = unicodedata.normalize('NFKD', sa).encode('ascii', 'ignore')
			data_record_dict = record_dict_value(data_record_dict, "SA", sa)

			# //*[@id="stats-page-body"]/div[3]/div[1]/div[3]/div[1]/div/div[13]
			svs_xpath = current_row_path + "/div/div[13]"
			svs = driver.find_element_by_xpath(svs_xpath).text
			svs = unicodedata.normalize('NFKD', svs).encode('ascii', 'ignore')
			data_record_dict = record_dict_value(data_record_dict, "Svs", svs)

			ga_xpath =  current_row_path + "/div/div[14]"
			ga = driver.find_element_by_xpath(ga_xpath).text
			ga = unicodedata.normalize('NFKD', ga).encode('ascii', 'ignore')
			data_record_dict =  record_dict_value(data_record_dict, "GA", ga)

			svp_xpath =  current_row_path + "/div/div[15]"
			svp = driver.find_element_by_xpath(svp_xpath).text
			svp = unicodedata.normalize('NFKD', svp).encode('ascii', 'ignore')
			data_record_dict =  record_dict_value(data_record_dict, "Sv%", svp)

			gaa_xpath =  current_row_path + "/div/div[16]"
			gaa = driver.find_element_by_xpath(gaa_xpath).text
			gaa = unicodedata.normalize('NFKD', gaa).encode('ascii', 'ignore')
			data_record_dict =  record_dict_value(data_record_dict, "GAA", gaa)

			# //*[@id="stats-page-body"]/div[3]/div[1]/div[3]/div[1]/div/div[17]/div
			toi_xpath =  current_row_path + "/div/div[17]/div"
			toi = driver.find_element_by_xpath(toi_xpath).text
			toi = unicodedata.normalize('NFKD', toi).encode('ascii', 'ignore')
			data_record_dict =  record_dict_value(data_record_dict, "TOI", toi)

			so_xpath =  current_row_path + "/div/div[18]"
			so = driver.find_element_by_xpath(so_xpath).text
			so = unicodedata.normalize('NFKD', so).encode('ascii', 'ignore')
			data_record_dict = record_dict_value(data_record_dict, "SO", so)

			g_xpath =  current_row_path + "/div/div[19]"
			g = driver.find_element_by_xpath(g_xpath).text
			g = unicodedata.normalize('NFKD', g).encode('ascii', 'ignore')
			data_record_dict =  record_dict_value(data_record_dict, "G", g)

			a_xpath =  current_row_path + "/div/div[20]"
			a = driver.find_element_by_xpath(a_xpath).text
			a = unicodedata.normalize('NFKD', a).encode('ascii', 'ignore')
			data_record_dict =  record_dict_value(data_record_dict, "A", a)

			p_xpath =  current_row_path + "/div/div[21]"
			p = driver.find_element_by_xpath(p_xpath).text
			p = unicodedata.normalize('NFKD', p).encode('ascii', 'ignore')
			data_record_dict =  record_dict_value(data_record_dict, "P", p)

			pim_xpath =  current_row_path + "/div/div[22]"
			pim = driver.find_element_by_xpath(pim_xpath).text
			pim = unicodedata.normalize('NFKD', pim).encode('ascii', 'ignore')
			data_record_dict =  record_dict_value(data_record_dict, "PIM", pim)

			data_record.append(data_record_dict)
			
		for data_record_line in data_record:
			txt_file.write(str(data_record_line))
			txt_file.write("\n")


def start_crawl(gameType, season):
	chrome_driver = find_chrome()
	search_page_driver = jump2search(chrome_driver, gameType, season)
			# jump2search(driver, gameType, season_num)
			# gameType = 2 for regular seasons, = 3 for playoffs
	data_directory = get_store_directory(season, gameType )
	if os.path.exists(data_directory):
		with open(data_directory, "a") as txt_file:
			crawl_data(txt_file, search_page_driver)
	else:
		with open(data_directory, "w") as txt_file:
			crawl_data(txt_file, search_page_driver)
	chrome_driver.close()


if __name__ == '__main__':
	for season in range (2015, 2016):
		for gameType in range(3, 4):
			start_crawl(gameType, season)
