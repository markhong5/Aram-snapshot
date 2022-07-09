from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
WINDOWSIZE = "1080,1080"
SCROLLSIZE = ".05"
os.environ["PATH"] = r"C:\Selenium Drivers\chromedriver_win32"

def create_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('disable-notifications')
    # chrome_options.add_argument("start-maximized");
    chrome_options.add_argument("headless")
    chrome_options.add_argument(f"--window-size={WINDOWSIZE}")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

driver = create_chrome_driver()
driver.get(fr"https://na.whatismymmr.com/overlordultimark")
mmr = driver.find_element("xpath", r"/html/body/container[2]/container[2]/container[1]/container/wrapper[2]/div[1]/span[1]")
rank = driver.find_element("xpath", r"/html/body/container[2]/container[2]/container[1]/container/wrapper[2]/div[3]")
print(mmr.text)
print(rank.text)
driver.quit()



