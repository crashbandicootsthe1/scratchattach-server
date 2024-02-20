import os
os.system("pip install flask")
from flask import Flask, render_template
from threading import Thread

app = Flask(__name__)

@app.route('/')
def site():
  return render_template('index.html')

def run():
  app.run('127.0.0.1', port=8808)

def keep_alive():
  t = Thread(target=run)
  t.start()
