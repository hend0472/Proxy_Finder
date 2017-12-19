import requests
import bs4
from random import choice
import selenium
from selenium import webdriver
import time
from multiprocessing.dummy import Pool
import datetime
import random


global proxy_delete_list, proxy_list


proxy_check = 'https://canihazip.com/'
proxy_list = []
proxy_delete_list = []


class bcolors:
	"""Sets color codes for text printing"""
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	FAILRED = '\033[31m'
	WARNING = '\033[93m'
	WHITET = '\033[97m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	REDBACK = '\033[41m'
	GREENBACK = '\033[42m'
	YELLOWT = '\033[33m'


def print_t(message, type_m):
	"""Just an improvement on regular print, makes it easier to track what's going on with color and timestamp"""
	time.sleep(.01)
	if str(type_m).lower() == 'hard fail':
		print('[' + str(datetime.datetime.now()) + '] ' + bcolors.REDBACK +  bcolors.YELLOWT + str(	message) +
			  bcolors.ENDC)
	elif str(type_m).lower() == 'hard pass':
		print('[' + str(datetime.datetime.now()) + '] ' + bcolors.GREENBACK + bcolors.WHITET + str(message) +
			  bcolors.ENDC)
	elif str(type_m).lower() == 'pass':
		print('[' + str(datetime.datetime.now()) + '] ' + bcolors.OKGREEN + str(message) + bcolors.ENDC)
	elif str(type_m).lower() == 'blue':
		print('[' + str(datetime.datetime.now()) + '] ' + bcolors.OKBLUE + str(message) + bcolors.ENDC)
	elif str(type_m).lower() == 'warn':
		print('[' + str(datetime.datetime.now()) + '] ' + bcolors.WARNING + str(message) + bcolors.ENDC)
	elif str(type_m).lower() == 'none':
		print('[' + str(datetime.datetime.now()) + '] ' + str(message))
	elif str(type_m).lower() == 'fail':
		print('[' + str(datetime.datetime.now()) + '] ' + bcolors.FAILRED + str(message) + bcolors.ENDC)
	else:
		print('SOMETHING FUCKED UP')
		print('[' + str(datetime.datetime.now()) + '] ' + message)


def find_my_ip():
	global my_ip_address
	response = requests.get(proxy_check)
	soup = bs4.BeautifulSoup(response.text, 'html.parser')
	my_ip_address = soup.find('pre').text.strip()


def find_proxies():
	try:
		print_t('PULLING LIST OF PROXIES. PLEASE WAIT.', 'warn')
		proxy_url = 'https://hidemy.name/en/proxy-list/?maxtime=2000&type=s#list'
		# driver = webdriver.Firefox()
		driver = webdriver.PhantomJS()
		time.sleep(2)
		driver.get(proxy_url)
		time.sleep(10)
		soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
		proxy_table = soup.find('tbody')
		for tr in proxy_table.find_all('tr'):
			tds = tr.find_all('td')
			ip_address = tds[0].text
			port = tds[1].text
			type = tds[4].text
			if type == 'HTTP, HTTPS' or type == 'HTTPS':
				# print(ip_address, port, type)
				http_proxy = 'http://' + str(ip_address) + ':' + str(port)
				https_proxy = 'https://' + str(ip_address) + ':' + str(port)
				proxy = {'https':https_proxy, 'http':http_proxy}
				proxy_list.append(proxy)
		# for i in range(20):
		for i in range(1, 5):
			print_t('PULLING PAGE ' + str(i), 'warn')
			next_page = driver.find_element_by_xpath('/html/body/div[1]/div/section[1]/div/div[4]/ul/li[1]/a')
			next_page.click()
			soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
			proxy_table = soup.find('tbody')
			for tr in proxy_table.find_all('tr'):
				tds = tr.find_all('td')
				ip_address = tds[0].text
				port = tds[1].text
				type = tds[4].text
				if type == 'HTTP, HTTPS' or type == 'HTTPS':
					# print(ip_address, port, type)
					http_proxy = 'http://' + str(ip_address) + ':' + str(port)
					https_proxy = 'https://' + str(ip_address) + ':' + str(port)
					proxy = {'https': https_proxy, 'http': http_proxy}
					proxy_list.append(proxy)
			time.sleep(1)
		print_t('THERE ARE ' + str(len(proxy_list)) + ' PROXIES.', 'pass')
		driver.quit()
		time.sleep(1)
	except:
		pass


def find_proxies_2():
	try:
		print_t('FINDING MORE PROXIES.', 'WARN')
		proxy_url = 'https://free-proxy-list.net/'
		driver = webdriver.PhantomJS()
		time.sleep(2)
		driver.get(proxy_url)
		time.sleep(2)
		soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
		proxy_table = soup.find('tbody')
		for tr in proxy_table.find_all('tr'):
			# print(tr.text)
			tds = tr.find_all('td')
			ip_address = tds[0].text
			port = tds[1].text
			type = tds[6].text.strip()
			# print(ip_address, port, type)
			if type == 'yes':
				# print(ip_address, port, type)
				http_proxy = 'http://' + str(ip_address) + ':' + str(port)
				https_proxy = 'https://' + str(ip_address) + ':' + str(port)
				proxy = {'https': https_proxy, 'http': http_proxy}
				proxy_list.append(proxy)
		for i in range(1, 14):
			print_t('PULLING PAGE ' + str(i), 'warn')
			next_page = driver.find_element_by_xpath('/html/body/section[1]/div/div[2]/div/div[3]/div[2]/div/ul/li[10]/a')
			next_page.click()
			time.sleep(2)
			soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
			proxy_table = soup.find('tbody')
			for tr in proxy_table.find_all('tr'):
				# print(tr.text)
				tds = tr.find_all('td')
				ip_address = tds[0].text
				port = tds[1].text
				type = tds[6].text.strip()
				# print(ip_address, port, type)
				if type == 'yes':
					# print(ip_address, port, type)
					http_proxy = 'http://' + str(ip_address) + ':' + str(port)
					https_proxy = 'https://' + str(ip_address) + ':' + str(port)
					proxy = {'https': https_proxy, 'http': http_proxy}
					proxy_list.append(proxy)

		print_t('THERE ARE ' + str(len(proxy_list)) + ' PROXIES.', 'PASS')
	except:
		pass


def find_proxies_3():
	try:
		print_t('FINDING MORE PROXIES.', 'WARN')
		proxy_url = 'http://proxydb.net/'
		proxy_url = 'http://proxydb.net/?protocol=https&ip_filter=&port_filter=&host_filter=&via_filter=&country_filter=&city_filter=&region_filter=&isp_filter='
		driver = webdriver.PhantomJS()
		time.sleep(2)
		driver.get(proxy_url)
		time.sleep(2)
		soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
		proxy_table = soup.find('tbody')
		for tr in proxy_table.find_all('tr'):
			tds = tr.find_all('a')
			# print(tds[0].text)
			proxy_info = tds[0].text
			http_proxy = 'http://' + proxy_info
			https_proxy = 'https://' + proxy_info
			proxy = {'https': https_proxy, 'http': http_proxy}
			proxy_list.append(proxy)
		for i in range(1, 20):
			try:
				print_t('PULLING PAGE ' + str(i), 'warn')
				next_page = driver.find_element_by_xpath('/html/body/div[2]/nav/a[2]/span[1]')
				next_page.click()
				time.sleep(2)
				soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
				proxy_table = soup.find('tbody')
				for tr in proxy_table.find_all('tr'):
					tds = tr.find_all('a')
					proxy_info = tds[0].text
					http_proxy = 'http://' + proxy_info
					https_proxy = 'https://' + proxy_info
					proxy = {'https': https_proxy, 'http': http_proxy}
					proxy_list.append(proxy)
			except:
				break
		print_t('THERE ARE ' + str(len(proxy_list)) + ' PROXIES.', 'PASS')
	except:
		pass


def find_proxies_4():
	try:
		print_t('FINDING MORE PROXIES.', 'WARN')
		proxy_url = 'https://www.sslproxies.org/'
		driver = webdriver.PhantomJS()
		time.sleep(2)
		driver.get(proxy_url)
		time.sleep(2)
		soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
		proxy_table = soup.find('tbody')
		for tr in proxy_table.find_all('tr'):
			# print(tr.text)
			tds = tr.find_all('td')
			ip_address = tds[0].text
			port = tds[1].text
			type = tds[6].text.strip()
			# print(ip_address, port, type)
			if type == 'yes':
				# print(ip_address, port, type)
				http_proxy = 'http://' + str(ip_address) + ':' + str(port)
				https_proxy = 'https://' + str(ip_address) + ':' + str(port)
				proxy = {'https': https_proxy, 'http': http_proxy}
				proxy_list.append(proxy)
		for i in range(1, 5):
			print_t('PULLING PAGE ' + str(i), 'warn')
			next_page = driver.find_element_by_xpath('/html/body/section[1]/div/div[2]/div/div[3]/div[2]/div/ul/li[8]/a')
			next_page.click()
			time.sleep(2)
			soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
			proxy_table = soup.find('tbody')
			for tr in proxy_table.find_all('tr'):
				# print(tr.text)
				tds = tr.find_all('td')
				ip_address = tds[0].text
				port = tds[1].text
				type = tds[6].text.strip()
				# print(ip_address, port, type)
				if type == 'yes':
					# print(ip_address, port, type)
					http_proxy = 'http://' + str(ip_address) + ':' + str(port)
					https_proxy = 'https://' + str(ip_address) + ':' + str(port)
					proxy = {'https': https_proxy, 'http': http_proxy}
					proxy_list.append(proxy)

		print_t('THERE ARE ' + str(len(proxy_list)) + ' PROXIES.', 'PASS')
	except:
		pass


def find_proxies_5():
	res = requests.get('https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt')
	proxy_list_2 = (res.text).split('\n')
	for proxy_ip in proxy_list_2:
		try:
			if proxy_ip[0].isdigit():
				proxy_ip = proxy_ip.split(' ')[0]
				http_proxy = 'http://' + str(proxy_ip)
				https_proxy = 'https://' + str(proxy_ip)
				proxy = {'https': https_proxy, 'http':http_proxy}
				proxy_list.append(proxy)
		except:
			pass


def random_proxy():
	return choice(proxy_list)


def check_proxies(proxy_item):
	try:
		# print(proxy_item)
		response = requests.get(proxy_check, proxies = proxy_item, timeout = 2)
		soup = bs4.BeautifulSoup(response.text, 'html.parser')
		ip_address = soup.find('pre').text.strip()
		if ip_address != my_ip_address:
			print_t('GOOD PROXY ' + ip_address, 'pass')
		else:
			proxy_delete_list.append(proxy_item)
	except:
		print_t('BAD PROXY. ADDING TO REMOVE LIST.', 'fail')
		proxy_delete_list.append(proxy_item)


def remove_bad_proxies():
	for proxy in proxy_delete_list:
		proxy_list.remove(proxy)


def populate_proxy_list():
	find_my_ip()
	find_proxies()
	find_proxies_2()
	find_proxies_3()
	find_proxies_4()
	find_proxies_5()
	print_t('CHECKING PROXIES...', 'warn')
	pool = Pool(64)
	pool.map(check_proxies, proxy_list)
	pool.close()
	pool.join()
	remove_bad_proxies()
	print_t('THERE ARE ' + str(len(proxy_list)) + ' PROXIES REMAINING.', 'pass')
	return proxy_list





if __name__ == '__main__':
	find_my_ip()
	find_proxies()
	find_proxies_2()
	find_proxies_3()
	find_proxies_4()
	find_proxies_5()
	print_t('CHECKING PROXIES...', 'warn')
	pool = Pool(64)
	pool.map(check_proxies, proxy_list)
	pool.close()
	pool.join()
	remove_bad_proxies()
	print_t('THERE ARE ' + str(len(proxy_list)) + ' PROXIES REMAINING.', 'pass')
