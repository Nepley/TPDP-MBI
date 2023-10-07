from flask import Flask, render_template, request
import webview
from battleData import BattleData
import json
import time

app = Flask(__name__)

## Init
tpdp = None

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/init")
def init():
	global tpdp
	print("Init...")
	if tpdp == None:
		tpdp = BattleData()
		datas = [{"type": "message", "data":"Application Ready"}]
		print("Game Found, Starting loop...")
	return datas

@app.route("/update")
def update():
	datas = []
	global tpdp
	time.sleep(1)

	if tpdp.getEnemyPuppetId() > 0:
		data = {"puppet": tpdp.getEnemyPuppet(), "style": tpdp.getEnemyPuppetStyle(), "weaknesses": tpdp.getEnemyTableWeaknesses()}
		datas.append({"type": "puppetData", "data": json.dumps(data)})

	return datas

if __name__ == "__main__":
	webview.create_window('TPDP-MBI', app, width=950, height=225, frameless=True)
	webview.start(gui='qt')