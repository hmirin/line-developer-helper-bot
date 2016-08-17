# -*- coding: utf-8 -*-
from flask import request
from flask import jsonify
from flask import app
from flask import Flask
import json
import datetime
import urllib
import urllib2
from config import env_config as config


app = Flask(__name__)

def mid_to_type(mid):
    if "u" == mid[0]:
        return 1
    elif "r" == mid[0]:
        return 2
    elif "c" == mid[0]:
        return 3

@app.route('/', methods=['POST'])
def respond():
    # preprocess request
    request_json = request.json
    for msg in request_json["result"]:
        mid = msg['content']['from']
        request_content = {
        "to": [mid],
        "toChannel": "1383378250", # Fixed  value
        "eventType": "138311608800106203", # Fixed value
        "content": {
            "contentType": 1,
            "toType": mid_to_type(mid),
            "text": "Your mid is " + mid
            }
        }
        url = 'https://trialbot-api.line.me/v1/events'
        body = json.dumps(request_content)
        header = {
        'Content-Type': 'application/json; charset=UTF-8',
        'X-Line-ChannelID': config["LINE_CHANNEL_ID"],
        'X-Line-ChannelSecret': config["LINE_CHANNEL_SECRET"],
        'X-Line-Trusted-User-With-ACL': config["LINE_CHANNEL_MID"],
        }
        req = urllib2.Request(url, body ,header)
        res = urllib2.urlopen(req)

if __name__ == '__main__':
    host = app.config.get('HOST', '0.0.0.0')
    port = app.config.get('PORT', 8080)

    # initialize
    app.run(host=host, port=port, threaded=True)
