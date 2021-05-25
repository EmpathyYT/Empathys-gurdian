from flask import Flask
from threading import Thread
import random 

app = Flask('')


@app.route('/')
def home():
	return "I'm alive and working!"


def run():
	app.run(host='0.0.0.0', port=random.randint(0000, 9999))


def keep_alive():
	t = Thread(target=run)
	t.start()