from selenium import webdriver
from selenium.webdriver.chrome.options import Options
WINDOWSIZE = "1080,1080"

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
#chrome_options.add_argument('disable-notifications')
# chrome_options.add_argument("start-maximized");
#chrome_options.add_argument("headless")
#chrome_options.add_argument(f"--window-size={WINDOWSIZE}")
#driver = webdriver.Chrome(options=chrome_options, executable_path=os.environ["PATH"])
driver = webdriver.Chrome(options=chrome_options)

