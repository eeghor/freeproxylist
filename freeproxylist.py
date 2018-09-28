from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re
import time

"""
Level 1 - Elite Proxy / Highly Anonymous Proxy: The web server can't detect whether you are using a proxy.
Level 2 - Anonymous Proxy: The web server can know you are using a proxy, but it can't know your real IP.
Level 3 - Transparent Proxy: The web server can know you are using a proxy and it can also know your real IP.

"""

class FreeProxies:

	BASE_URL_ = 'https://free-proxy-list.net'

	def __init__(self, anonymity='elite proxy', https='yes', wait=30):

		assert anonymity in ['elite proxy', 'transparent', 'anonymous'], print('choose correct anonymity')

		self.anonymity = anonymity
		self.https = https
		self.wait  = wait

		self.lst = []

	def get(self):

		options = webdriver.ChromeOptions()
		options.add_argument('disable-notifications')
		options.add_argument('headless')

		self.driver = webdriver.Chrome('webdriver/chromedriver', chrome_options=options)

		self.driver.get(FreeProxies.BASE_URL_)
		
		WebDriverWait(self.driver, self.wait).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 
				f'#proxylisttable>tfoot>tr>th:nth-child(5)>select>option[value="{self.anonymity}"]'))).click()
		
		time.sleep(3)

		WebDriverWait(self.driver, self.wait).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 
				f'#proxylisttable > tfoot > tr > th.hx.ui-state-default > select > option[value="{self.https}"]'))).click()
		
		time.sleep(3)

		info_ = WebDriverWait(self.driver, self.wait).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 
									'#proxylisttable_info'))).text.strip().lower()

		nres = int(re.search(r'(?<=of)\s+\d+\s+(?=entries)', info_).group(0).strip())  #  of 145 entries

		print(f'found {nres} proxies')

		page_numbers = [int(_.text.strip()) for _ in self.driver.find_elements_by_css_selector('#proxylisttable_paginate>ul>li') 
							if _.text.strip().isdigit()]

		print('collecting...')

		for page in range(1, max(page_numbers) + 1):

			row_ = 1

			while True:

				try:
					row_text = self.driver.find_element_by_css_selector(f'#proxylisttable>tbody>tr:nth-child({row_})').text.strip()
					
					if row_text not in self.lst:
						self.lst.append(row_text)
					row_ += 1
				
				except:	
					# can't get a row - time to go to the next page
					for a in self.driver.find_elements_by_css_selector('#proxylisttable_paginate>ul>li.fg-button.ui-button.ui-state-default>a'):
	
						try:
							if int(a.text.strip()) == page + 1:
								a.click()
								time.sleep(5)
								break
						except:
							continue
					break

		if len(self.lst) != nres:
			print(f'collected not as many proxies as expected: {len(self.lst)}!')
		else:
			print('done')

		self.driver.close()

		return self

	def save(self, to_where='proxies.txt'):

		with open(to_where, 'w') as f:	
			for _ in self.lst:
				f.write('{}:{}\n'.format(*_.split()[:2]))

		print(f'saved to {to_where}')

		return self

if __name__ == '__main__':

	FreeProxies().get().save()
