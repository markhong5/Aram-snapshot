# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import discord
from discord.ext import tasks
import time
import difflib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from riotwatcher import LolWatcher, ApiError
from dotenv import load_dotenv
from AramMessages import AramMessage, VALUES
import requests


WINDOWSIZE = "1080,1080"
SCROLLSIZE = ".05"



class AramBot(discord.Client):
    def __init__(self, champ_snapshot_path, chrome_driver_path, *args, **kwargs):
        intents = discord.Intents.all()
        super().__init__(intents=intents, *args, **kwargs)
        self.champ_list = self.get_champ_list()
        self.champ_snapshot_path = champ_snapshot_path
        #os.environ["PATH"] = chrome_driver_path

    # async def setup_hook(self) -> None:
    #     # start the task to run in the background
    #     self.update_champ_builds.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    # @tasks.loop(hours=168)  # task runs every 7 days
    # async def update_champ_builds(self):
    #     self.update_snapshots()

    # @update_champ_builds.before_loop
    # async def before_my_task(self):
    #     await self.wait_until_ready()  # wait until the bot is ready

    def create_chrome_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('disable-notifications')
        # chrome_options.add_argument("start-maximized");
        chrome_options.add_argument("headless")
        chrome_options.add_argument(f"--window-size={WINDOWSIZE}")
        #driver = webdriver.Chrome(options=chrome_options, executable_path=os.environ["PATH"])
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def create_aram_snapshot(self, driver, champ_name):
        print(champ_name)
        driver.get(fr"https://app.mobalytics.gg/lol/champions/{champ_name}/aram-builds")
        try:
            collpase_bar = driver.find_element("class name", "m-1yjfmri")
            collpase_bar.click()
            time.sleep(.5)
        except NoSuchElementException:
            pass

        driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {SCROLLSIZE})")
        driver.save_screenshot(os.path.join(self.champ_snapshot_path, str(champ_name) + ".png"))

    def get_snapshots(self, driver):
        with open("champion_list.txt", "r+") as f:
            f.truncate(0)
            #clears the champ file
        load_dotenv()
        API_KEY = os.environ['LEAGUE_API']
        lol_watcher = LolWatcher(API_KEY)
        my_region = 'na1'
        versions = lol_watcher.data_dragon.versions_for_region(my_region)
        champions_version = versions['n']['champion']
        current_champ_list = lol_watcher.data_dragon.champions(champions_version)

        current_champ_list = [champ.lower() for champ in current_champ_list["data"]]
        for champ in current_champ_list:
            self.create_aram_snapshot(driver, champ)
            with open("champion_list.txt", "a") as f:
                f.write(champ)
                f.write("\n")

    def get_champ_list(self):
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

    def update_snapshots(self):
        print("Updating snapshots")
        driver = self.create_chrome_driver()
        self.get_snapshots(driver)
        driver.quit()
        print("Finished updating snapshots")

    def get_mmr(self, name):
        driver = self.create_chrome_driver()
        driver.get(fr"https://na.whatismymmr.com/{name}")
        mmr = driver.find_element("xpath",
                                  r"/html/body/container[2]/container[2]/container[1]/container/wrapper[2]/div[1]/span[1]").text
        rank = driver.find_element("xpath",
                                   r"/html/body/container[2]/container[2]/container[1]/container/wrapper[2]/div[3]").text
        driver.quit()
        if mmr != "N/A":
            return f"Summoner: {name}\nMMR: {mmr}\nMMR is equivalent to {rank}"
        else:

            return f"Could not find summoner {name} ARAM MMR"

def run_bot(champ_snapshot_path, chrome_driver_path):
    #load_dotenv(find_dotenv())
    TOKEN = os.environ['DISCORD_TOKEN']
    assert type(TOKEN) == str
    client = AramBot(champ_snapshot_path, chrome_driver_path)

    @client.event
    async def on_message(message):
        #print(message.author)
        #Kero#4827
        if message.channel.id == 994681128965386241 and len(message.content) != 0:
            if message.author == client.user:
                return
            print(message.author)
            aram_message = AramMessage(message.author, message.content)
            type_of_message = aram_message.process_message()
            if type_of_message == VALUES["LEAGUE"]:

                file_name = aram_message.aram_snapshot(client.champ_list, client.champ_snapshot_path)
                try:
                    await message.channel.send(file=discord.File(file_name))
                except FileNotFoundError:
                    print("file not found")
                    await message.channel.send(file_name)
            elif type_of_message == VALUES["MMR"]:
                mmr_message = client.get_mmr(aram_message.content)
                await message.channel.send(mmr_message)
            elif type_of_message == VALUES["APEX"]:
                load_dotenv()
                APEX_TOKEN = os.environ['APEX_API']
                await message.channel.send(aram_message.apex_map(APEX_TOKEN))
            elif type_of_message == VALUES["SPECIAL"]:
                await message.channel.send(file=discord.File(aram_message.special_message(client.champ_snapshot_path)))
            elif type_of_message == VALUES["UPDATE"]:
                print("running update")
                await message.channel.send("Updating Snapshots")
                client.update_snapshots()
                await message.channel.send(f"Snapshots are Updated")
                
            elif type_of_message == VALUES["NONE"]:
                 await message.channel.send(f"Not an ARAM BOT Command")
        else:
            print("INVALID MESSAGE")
                

    print("running client")
    client.run(TOKEN)
if __name__ == '__main__':
    pass
    # load_dotenv()
    # APEX_TOKEN = os.getenv('APEX_API')
    # response = requests.get(f"https://api.mozambiquehe.re/maprotation?auth={APEX_TOKEN}")
    # from pprint import pprint
    # pprint(response.json()["current"]["map"])
    # '        "remainingTimer": "01:21:25"\n'
    # driver = create_chrome_driver()
    # create_aram_snapshot(driver, "aatrox")
    # #update_snapshots(driver)
    # driver.quit()
    #run_bot()






