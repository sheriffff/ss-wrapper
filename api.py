from flask import Flask
from flask import request

from selenium import webdriver
from crawler import SSocialCrawler
from media.music import play_clip
from users_data import users

app = Flask(__name__)

counter = 0
running = False


@app.route("/")
def index():
    global counter
    counter += 1
    return f"<h1>Hi {counter}</h1>"
#    return f"hi {counter}"


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

    play_clip("media/beep.wav")

    return "READY!"


@app.route('/testpost', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("posted")
        return {"tipo_llamada": "post"}
    else:
        print("gotten")
        return {"tipo_llamada": "get"}
    print("hola")
    print(request.data)


app.run(host="0.0.0.0")
