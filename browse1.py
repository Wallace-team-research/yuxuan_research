from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time

def is_element_present(driver, selector, value):
	try:
		driver.find_element(by=selector, value=value)
		return True
	except NoSuchElementException:
		return False

info = open("anhui1.txt", "r")
browser = webdriver.Chrome()

line = info.readline().rstrip('\n')
while line != '':
	# separate info from the text file
	items = line.split(" ")
	entname = items[0]
	outfile = open(entname+".txt", "w", encoding='utf-8')
	url = items[1]
	options = items[2:]
	browser.get(url)

	for value in options: # station select
		while not is_element_present(browser, By.NAME, 'DropPk'):
			time.sleep(0.5)
			continue
		select = Select(browser.find_element_by_name('DropPk'))
		select.select_by_value(value)
		while not is_element_present(browser, By.ID, 'txtkssj'):
			time.sleep(0.5)
			continue
		begin_date = browser.find_element_by_id('txtkssj')
		begin_date.clear()
		begin_date.send_keys("2014-11-30 00:00:00")
		while not is_element_present(browser, By.ID, 'Button2'):
			time.sleep(0.5)
			continue
		browser.find_element_by_id('Button2').click() # submit the start date
		time.sleep(3) # wait for page to load

		# find the total pages that we need to go over
		while not is_element_present(browser, By.XPATH, "//*[@id='AspNetPager1']/div[2]"):
			time.sleep(0.5)
			continue
		page_number = browser.find_element_by_xpath("//*[@id='AspNetPager1']/div[2]").get_attribute('innerHTML')
		pages = page_number.split(" ")
		page = pages[0].lstrip().split("/")[1]
		max_page = int(page[:-1])
		print("total: {} pages".format(max_page))
		
		#===write first page with header===#
		while not is_element_present(browser, By.XPATH, "//*[@id='AspNetPager1']/div[1]/a[12]"):
			time.sleep(0.5)
			continue
		browser.find_element_by_xpath("//*[@id='AspNetPager1']/div[1]/a[12]").click() # next page button
		while not is_element_present(browser, By.XPATH, "//table[@class='app_table']"):
			time.sleep(1)
			continue
		table = browser.find_element_by_xpath("//table[@class='app_table']") # data table
		soup = BeautifulSoup(table.get_attribute("innerHTML"), "lxml")
		trs = soup.find_all('tr')
		header = trs[0].text.strip()+trs[1].text.strip()+"\n"
		outfile.write(header)
		for tr in trs[2:]: # write other data (12 entries/page)
			txt = tr.text.strip()+"\n"
			outfile.write(txt)

		#===write following pages data===#
		for i in range(2, max_page-6): # pagination
			while not is_element_present(browser, By.XPATH, "//*[@id='AspNetPager1']/div[1]/a[12]"):
				time.sleep(0.5)
				continue
			browser.find_element_by_xpath("//*[@id='AspNetPager1']/div[1]/a[12]").click() # next page button
			while not is_element_present(browser, By.XPATH, "//table[@class='app_table']"):
				time.sleep(1)
				continue
			table = browser.find_element_by_xpath("//table[@class='app_table']") # data table
			soup = BeautifulSoup(table.get_attribute("innerHTML"), "lxml")
			trs = soup.find_all('tr')
			for tr in trs[2:]: # write other data (12 entries/page)
				txt = tr.text.strip()+"\n"
				outfile.write(txt)

		#===write the last 7 pages data===#
		for i in range(max_page-6, max_page+1): # pagination
			while not is_element_present(browser, By.XPATH, "//*[@id='AspNetPager1']/div[1]/a[10]"):
				time.sleep(0.5)
				continue
			browser.find_element_by_xpath("//*[@id='AspNetPager1']/div[1]/a[10]").click() # next page button
			while not is_element_present(browser, By.XPATH, "//table[@class='app_table']"):
				time.sleep(1)
				continue
			table = browser.find_element_by_xpath("//table[@class='app_table']") # data table
			soup = BeautifulSoup(table.get_attribute("innerHTML"), "lxml")
			trs = soup.find_all('tr')
			for tr in trs[2:]: # write other data (12 entries/page)
				txt = tr.text.strip()+"\n"
				outfile.write(txt)

	outfile.close()
	print(entname + "is done!")
	line = info.readline().rstrip('\n')

browser.close()
browser.quit()