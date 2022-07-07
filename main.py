# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from riotwatcher import LolWatcher, ApiError
from pprint import pprint
import discord
from dotenv import load_dotenv
import time
from selenium.common.exceptions import NoSuchElementException
import difflib

#like the selenium web driver, but is better at detecting adds
os.environ["PATH"] += r"C:\Selenium Drivers\chromedriver_win32"
WINDOWSIZE = "1600,1200"
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
    print(champ_name)
    driver.get(fr"https://app.mobalytics.gg/lol/champions/{champ_name}/aram-builds")
    try:
        collpase_bar = driver.find_element("class name", "m-1yjfmri")
        collpase_bar.click()
        time.sleep(.5)
    except NoSuchElementException:
        pass

    driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {SCROLLSIZE})")
    driver.save_screenshot(fr"C:\Users\overl\PycharmProjects\AramSnapshot\champ_snapshots\{champ_name}.png")

def update_snapshots(driver):
    load_dotenv()
    API_KEY = os.getenv('LEAGUE_API')
    lol_watcher = LolWatcher(API_KEY)
    my_region = 'na1'
    versions = lol_watcher.data_dragon.versions_for_region(my_region)
    champions_version = versions['n']['champion']
    current_champ_list = lol_watcher.data_dragon.champions(champions_version)

    current_champ_list = [champ.lower() for champ in current_champ_list["data"]]
    for champ in current_champ_list:
        create_aram_snapshot(driver, champ)
        with open("champion_list.txt", "a") as f:
            f.write(champ)
            f.write("\n")

def run_bot():
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    client = discord.Client()
    champ_list = []
    with open("champion_list.txt", "r") as f:
        champ_string = f.read()
    for champ in champ_string.split("\n"):
        champ_list.append(champ)

    champ_list.append("wukong")

    @client.event
    async def on_message(message):
        #print(message.author)#Kero#4827
        if message.channel.id == 994672415315607553:
            if message.author == client.user:
                return

            if message.content[0] == "!":
                champ_name = message.content[1:]
                close_matches = difflib.get_close_matches(champ_name, champ_list, n=3, cutoff=0.4)
                if len(close_matches) > 0:
                    champ_name = close_matches[0]
                    if champ_name == "wukong":
                        champ_name = "monkeyking"

                    await message.channel.send(
                        file=discord.File(fr"C:\Users\overl\PycharmProjects\AramSnapshot\champ_snapshots\{champ_name}.png"))
                else:
                    await message.channel.send(f"could not find any close matches. Try:{difflib.get_close_matches(champ_name, champ_list, n=3, cutoff=0.1)}")



    client.run(TOKEN)

if __name__ == '__main__':
    driver = create_chrome_driver()
    #update_snapshots(driver)
    driver.quit()
    #run_bot()
    # test = "drmundo dr_mundo"
    #
    # word = "dr MunDo"
    # champ_list = []
    # with open("champion_list.txt", "r") as f:
    #     champ_string = f.read()
    # for champ in champ_string.split("\n"):
    #     champ_list.append(champ)
    # print(difflib.get_close_matches(word, champ_list, n=3, cutoff=0.4))




