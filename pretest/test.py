from selenium import webdriver
import time

driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(15)
driver.get('http://www.mobileindex.com/mi-chart/top-charts/global-chart-by-market')


driver.maximize_window()
time.sleep(1)

driver.find_element_by_css_selector('.disabled-border~ .option+ .option .small label').click()
time.sleep(5)

driver.find_element_by_css_selector('.false:nth-child(3)').click()
time.sleep(5)



driver.quit()