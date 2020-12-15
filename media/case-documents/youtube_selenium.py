from selenium import webdriver
import time

browser = webdriver.Firefox()

url = "https://youtube.com"

browser.get(url)

#time.sleep(5)

input_youtube = browser.find_element_by_css_selector('.ytd-searchbox')

input_youtube.send_keys("reynmen melek")

button = browser.find_element_by_xpath('.style-scope.ytd-searchbox')

button.click()

time.sleep(3)

browser.close()


