# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
from selenium import webdriver
from riotwatcher import LolWatcher, ApiError
from pprint import pprint
#like the selenium web driver, but is better at detecting adds
os.environ["PATH"] += r"C:\Selenium Drivers\chromedriver_win32"
WINDOWSIZE = "1080,1080"
SCROLLSIZE = ".05"
API_KEY = r"RGAPI-442e7a6b-3dc2-4500-8b8a-4abe070cdc22"
def create_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('disable-notifications')
    #chrome_options.add_argument("start-maximized");
    chrome_options.add_argument("headless")
    chrome_options.add_argument(f"--window-size={WINDOWSIZE}")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def create_aram_snapshot(driver, champ_name):
    print(champ_name)
    driver.get(fr"https://app.mobalytics.gg/lol/champions/{champ_name}/aram-builds")
    driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {SCROLLSIZE})")
    driver.save_screenshot(fr"C:\Users\overl\PycharmProjects\AramSnapshot\champ_snapshots\{champ_name}.png")

def update_snapshots(driver):
    lol_watcher = LolWatcher(API_KEY)
    my_region = 'na1'
    versions = lol_watcher.data_dragon.versions_for_region(my_region)
    champions_version = versions['n']['champion']
    current_champ_list = lol_watcher.data_dragon.champions(champions_version)

    current_champ_list = [champ.lower() for champ in current_champ_list["data"]]
    for champ in current_champ_list:
        create_aram_snapshot(driver, champ)

if __name__ == '__main__':
    driver = create_chrome_driver()

    driver.quit()



