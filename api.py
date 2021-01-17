from flask import Flask
from flask import request

from selenium import webdriver
from crawler import SSocialCrawler
from music import play_clip
from users_data import users

app = Flask(__name__)


@app.route("/")
def index():
    return "hi"


@app.route("/run")
def run():
    username = request.args.get('username')
    user_data = users.get(username)

    if user_data is None:
        return f"Non-saved user: {username}"

    print(f"Running for {username}: {user_data}")

    driver = webdriver.Chrome("./chromedriver")

    ss = SSocialCrawler(driver, user_data)
    ss.run_until_success()

    play_clip("./beep.wav")

    return "READY!"


app.run()
