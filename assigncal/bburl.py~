from selenium import webdriver
from selenium.webdriver.common import keys
import sys

driver = webdriver.Firefox()
driver.get("https://blackboard.princeton.edu")

driver.find_element_by_xpath('//*[@title="I have a valid Princeton NetID and Password"]').click()
currentURL = driver.current_url
print(currentURL)
driver.close()
