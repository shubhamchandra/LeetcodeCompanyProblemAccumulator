from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time 
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options



'''

Download chromium driver for browser: http://chromedriver.storage.googleapis.com/index.html
https://stackoverflow.com/questions/8255929/running-selenium-webdriver-python-bindings-in-chrome

'''



COMPANY = 'amazon'
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.

driver = webdriver.Chrome(chrome_options=options)
driver.get("https://leetcode.com/company/{}/".format(COMPANY))
driver.find_element(By.ID, 'id_login').send_keys('myemail@yahoo.com')
driver.find_element(By.ID, 'id_password').send_keys('mypassword')
xpath='//*[@id="signin_btn"]'
button = driver.find_element(By.XPATH, xpath)
driver.execute_script("arguments[0].click();", button)
table_xpath ="//*[@class='table__XKyc']"


timeout = 120
try:
    element_present = EC.presence_of_element_located((By.XPATH, "//*[@class='title__PM_F']") )
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load")

table = driver.find_element(By.CSS_SELECTOR, "table.table__XKyc")


problems = []
cnt = 0
for row in table.find_elements(By.XPATH, ".//tr"):
	links = row.find_elements(By.XPATH, ".//td[3]/div/a")
	href = [link.get_attribute('href') for link in links]
	if len(href) > 0:
		problems.append(href[0])
	
opened = 0

problem_details = []


def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""


try:
	for prob in problems:
		
		driver.execute_script("window.open('');")

		# Switch to the new window and open new URL
		driver.switch_to.window(driver.window_handles[1])
		driver.get(prob)
		element_present = EC.presence_of_element_located((By.CSS_SELECTOR, ".css-5wdlwo-TabViewHeader .title__3f2k") )
		WebDriverWait(driver, timeout).until(element_present)
		time.sleep(3)
		discuss_tab = driver.find_elements(By.XPATH, "//*[@class='css-1lexzqe-TabHeaderContainer e5i1odf2']/div[3]//span[@class='title__3f2k']")[0]
		discuss_str = discuss_tab.text
		discuss_str = find_between_r(discuss_str, '(', ')')
		
		# Closing new_url tab
		company_header = driver.find_element(By.CSS_SELECTOR, "div.header__2X5E")
		driver.execute_script("arguments[0].click();", company_header)
		time.sleep(3)
		companies = driver.find_elements(By.XPATH, "//div[@class='company-tag-wrapper__1rBy']/a")	
		companies_count = []
		for company in companies:  
			spans = company.find_elements(by=By.CSS_SELECTOR, value='span')
			spans = [span.text for span in spans]
			companies_count.append(spans)
		try:
			span = list(filter(lambda span: span[0].lower() == COMPANY, companies_count))[0]
			problem_details.append({'Problem': prob, 'company': span[0], 'Frequency': int(span[-1]), 'Discuss': discuss_str})	
			print(prob, span, discuss_str)
		except:
			print('exception {}'.format(prob))		
		driver.close()
		  
		# Switching to old tab
		driver.switch_to.window(driver.window_handles[0])

except TimeoutException:
    print("Timed out waiting for page to load")
driver.quit()

problem_details.sort(key=lambda detail: detail['Frequency'], reverse=True)
print(problem_details)
df = pd.DataFrame.from_dict(problem_details) 
CSV_PATH = '/home/shubham/Downloads/AmazonLeetcode.csv'
df.to_csv (CSV_PATH, index = False, header=True)


