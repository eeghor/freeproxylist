from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

options = webdriver.ChromeOptions()
options.add_argument('disable-notifications')
# options.add_argument('headless')

"""
Level 1 - Elite Proxy / Highly Anonymous Proxy: The web server can't detect whether you are using a proxy.
Level 2 - Anonymous Proxy: The web server can know you are using a proxy, but it can't know your real IP.
Level 3 - Transparent Proxy: The web server can know you are using a proxy and it can also know your real IP.

"""

class FreeProxies:

	DRIVER_ = webdriver.Chrome('webdriver/chromedriver', chrome_options=options)
	BASE_URL_ = 'https://free-proxy-list.net'

	def __init__(self, anonymity='elite proxy'):

		assert anonymity in ['elite proxy', 'transparent', 'anonymous'], print('choose correct anonymity')

		self.anonymity = anonymity

		self.lst = []

	def get(self):

		FreeProxies.DRIVER_.get(FreeProxies.BASE_URL_)
		
		WebDriverWait(FreeProxies.DRIVER_, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 
			f'#proxylisttable > tfoot > tr > th:nth-child(5) > select>option[value="{self.anonymity}"]'))).click()
		time.sleep(3)

		print(WebDriverWait(FreeProxies.DRIVER_, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 
			'#proxylisttable_info'))).text)

		page_numbers = [int(_.text.strip()) for _ in FreeProxies.DRIVER_.find_elements_by_css_selector('#proxylisttable_paginate > ul > li') 
							if _.text.strip().isdigit()]

		for page in range(max(page_numbers)):

			print('page ', page)

			# collect 

			while True:

				row_ = 1

				try:

					self.lst.append(FreeProxies.DRIVER_.find_element_by_css_selector(f'#proxylisttable > tbody > tr:nth-child({row_})').text)
					row_ += 1
				
				except:	

					for a in FreeProxies.DRIVER_.find_elements_by_css_selector('#proxylisttable_paginate >ul> li.fg-button.ui-button.ui-state-default>a'):
	
						try:
							next_page = int(a.text.strip())
							if next_page == page + 1:
								a.click()
								time.sleep(5)
								break
						except:
							continue
	
					break

		print(f'total proxies: {len(self.lst)}')


if __name__ == '__main__':

	FreeProxies().get()




