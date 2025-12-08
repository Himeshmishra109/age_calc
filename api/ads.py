from flask import Flask, redirect

app = Flask(__name__)

@app.route('/ads.txt')
def ads_txt():
    return redirect("https://srv.adstxtmanager.com/19390/clackmasterpro.online", code=302)

handler = app
