# -*- coding: utf-8 -*-
import re

class Config(object):

    SERVER = "https://prod1.gp.kardia.winyourgames.com:9090/"
    PAY_SERVER = "http://prod.kardia.winyourgames.com:9080/"
    CENTER_SERVER = "https://prod.kardia.winyourgames.com:9099/"

    payloads = {
      "isp": "WiredSSID",
      "loginType": "player",
      "sdkUid": "",
      "reqid": 0,
      "platform": "ANDROID",
      "reqsid": 0,
      "deviceId": "",
      "channel": "FUNPLUS",
      "sdkToken": "",
      "imei": "unknow",
      "network": "WIFI",
      "osType": "ANDROID",
      "tjChannel": "tjDYD",
      "token": ""
    }
    
    def __init__(self):
        self.serverId = 2