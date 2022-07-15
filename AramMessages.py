import difflib
import os
import requests
import time
VALUES = {
    "LEAGUE": 1,
    "APEX": 2,
    "SPECIAL": 3,
    "UPDATE": 4,
    "MMR":5,
    "NONE": -1,
}
SPECIAL = {"tyler":"aphelios", "jose":"bard", "gianni":"rengar", "soni":"akali"}
class AramMessage:
    def __init__(self, author, message):
        self.author = str(author)
        self.message = message
        self.content = message[1:]

    def process_message(self):
        if self.message.startswith("!"):
            if self.message[1:] in SPECIAL:
                return VALUES["SPECIAL"]
            elif self.message.startswith("!mmr"):
                #correct way
                self.content = " ".join(self.message.split()[1:])
                return VALUES["MMR"]
            else:
                return VALUES["LEAGUE"]
        elif self.message.startswith("?map"):
            return VALUES["APEX"]
        elif self.message == "~update" and self.author == "Kero#4827":
            return VALUES["UPDATE"]
        else:
            return VALUES["NONE"]

    def aram_snapshot(self, champ_list, champ_snapshot_path):
        champ_name = self.content
        close_matches = difflib.get_close_matches(champ_name, champ_list, n=3, cutoff=0.6)
        if len(close_matches) > 0:
            champ_name = close_matches[0]
            if champ_name == "wukong":
                champ_name = "monkeyking"
            return os.path.join(champ_snapshot_path, str(champ_name) + ".png")
        else:
            return f"could not find any close matches. Try:{difflib.get_close_matches(champ_name, champ_list, n=3, cutoff=0.3)}"

    def special_message(self, champ_snapshot_path):
        return os.path.join(champ_snapshot_path, SPECIAL[self.content] + ".png")

    def apex_map(self, apex_api):
        response = requests.get(f"https://api.mozambiquehe.re/maprotation?auth={apex_api}")
        time.sleep(.5)
        map_info = response.json()
        current_map = map_info["current"]["map"]
        remaining_time = map_info["current"]["remainingTimer"]
        next_map = map_info["next"]["map"]
        return f"Current Map: {current_map}\nTime Remaining: {remaining_time}\nNext Map: {next_map}"

