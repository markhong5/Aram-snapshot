# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import discord
from discord.ext import tasks
import time
import difflib
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from riotwatcher import LolWatcher, ApiError
from pprint import pprint
from dotenv import load_dotenv
#LINUX
#like the selenium web driver, but is better at detecting adds
#need to change
#WINDOWs = r"C:\Selenium Drivers\chromedriver_win32"
os.environ["PATH"] += r"/lib/chromium-browser/chromedriver"
WINDOWSIZE = "1080,1080"
SCROLLSIZE = ".05"
#linux: /home/mark/Desktop/python_apps/discord_bot/Aram-snapshot/champ_snapshots/{champ_name}.png
#windows: C:\Users\overl\PycharmProjects\AramSnapshot\champ_snapshots\{champ_name}.png
LINUX = R"/home/mark/Desktop/python_apps/discord_bot/Aram-snapshot/champ_snapshots/"
#WINDOWS = R"C:\Users\overl\PycharmProjects\AramSnapshot\champ_snapshots\"


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
    driver.save_screenshot(LINUX + str(champ_name) + ".png")

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




def get_champ_list():
    champ_list = []
    with open("champion_list.txt", "r") as f:
        champ_string = f.read()
    for champ in champ_string.split("\n"):
        if champ == "":
            pass
        else:
            champ_list.append(champ)
    champ_list.append("wukong")
    return champ_list

def update_snapshots():
    print("Updating snapshots")
    driver = create_chrome_driver()
    update_snapshots(driver)
    driver.quit()
    print("Finished updating snapshots")
class AramBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.champ_list = get_champ_list()

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.update_champ_builds.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    @tasks.loop(hours=168)  # task runs every 7 days
    async def update_champ_builds(self):
        update_snapshots()

    @update_champ_builds.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot is ready


def run_bot():
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    client = AramBot()

    @client.event
    async def on_message(message):
        #print(message.author)#Kero#4827
        if message.channel.id == 994681128965386241:
            if message.author == client.user:
                return
            if len(message.content) != 0 and message.content[0] == "!":
                if message.author == "Kero#4827" and message.content[1:] == "update":
                    update_snapshots()
                    await message.channel.send(f"Updated Snapshots")
                else:
                    champ_name = message.content[1:]
                    close_matches = difflib.get_close_matches(champ_name, client.champ_list, n=3, cutoff=0.6)
                    if len(close_matches) > 0:
                        champ_name = close_matches[0]
                        if champ_name == "wukong":
                            champ_name = "monkeyking"

                        await message.channel.send(file=discord.File(LINUX + str(champ_name) + ".png"))
                    else:
                        await message.channel.send(f"could not find any close matches. Try:"
                                                   f"{difflib.get_close_matches(champ_name,  client.champ_list, n=3, cutoff=0.1)}")
        client.run(TOKEN)
if __name__ == '__main__':
    # driver = create_chrome_driver()
    # create_aram_snapshot(driver, "aatrox")
    # #update_snapshots(driver)
    # driver.quit()
    run_bot()






