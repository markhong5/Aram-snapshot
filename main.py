# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
from selenium import webdriver
#import undetected_chromedriver as webdriver
#like the selenium web driver, but is better at detecting adds
os.environ["PATH"] += r"C:\Selenium Drivers\chromedriver_win32"
WINDOWSIZE = "1080,1080"
SCROLLSIZE = ".05"

def create_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('disable-notifications')
    #chrome_options.add_argument("start-maximized");
    chrome_options.add_argument("headless")
    chrome_options.add_argument(f"--window-size={WINDOWSIZE}")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def create_aram_snapshot(driver, champ_name):
    driver.get(fr"https://app.mobalytics.gg/lol/champions/{champ_name}/aram-builds")
    driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {SCROLLSIZE})")
    driver.save_screenshot(fr"C:\Users\overl\PycharmProjects\AramSnapshot\champ_snapshots\{champ_name}.png")
    driver.close()

if __name__ == '__main__':
    #SET UP CHROME ENVIRNOMENT
    driver = create_chrome_driver()
    create_aram_snapshot(driver, "ashe")
    # Disables popups in chrome



    # #increases load speed
    # options = Options()
    # options.page_load_strategy = 'none'




