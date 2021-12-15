from selenium import webdriver
from bs4 import BeautifulSoup
import getpass
from selenium.webdriver.common.keys import Keys

userid = str(input("Enter email address or number with country code: "))
password = getpass.getpass('Enter your password:')


import pickle
driver_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/chromedriver.exe"
brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

option = webdriver.ChromeOptions()
option.binary_location = brave_path
# option.add_argument("--incognito") OPTIONAL
# option.add_argument("--headless") OPTIONAL

# Create new Instance of Chrome
driver = webdriver.Chrome(executable_path=driver_path, chrome_options=option)


driver.get("https://www.facebook.com/login")
driver.implicitly_wait(6)
driver.find_element_by_xpath("""//*[@id="email"]""").send_keys(userid)
driver.find_element_by_xpath("""//*[@id="pass"]""").send_keys(password)
driver.find_element_by_xpath("""//*[@id="loginbutton"]""").click()
pickle.dump( driver.get_cookies() , open("session.pkl","wb"))
driver.get("https://www.facebook.com/") #Enter any of your connection profile Link

pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))



