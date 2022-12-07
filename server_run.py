from main import run_bot
import os
champ_snapshot_path = r"champ_snapshots"
chrome_driver_path = r"/chromedriver_win32/chromedriver.exe"

try:
    run_bot(champ_snapshot_path, chrome_driver_path)
except:
    os.system("kill 1")

