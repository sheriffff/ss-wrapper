from selenium import webdriver

from crawler import SSocialCrawler
from media.music import play_clip
from users_data import users

name = "mama"

user_data = users[name]
driver = webdriver.Chrome("./chromedriver")

ss = SSocialCrawler(driver, user_data)
ss.run_until_success()

play_clip("media/beep.wav")

print("END")
