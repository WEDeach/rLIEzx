# -*- coding: utf-8 -*-
from datetime import datetime, date
from random import randint
from Crypto.Cipher import AES
import base64, json, hashlib

import json, shutil, time, os, base64, tempfile
    
class Models(object):
        
    def __init__(self):
        pass

    def log(self, text):
        try:
            print("[%s] %s" % (str(datetime.now()), text))
        except:
            print("[%s] LOG ERROR" % (str(datetime.now())))

    def saveFile(self, path, raw):
        with open(path, 'wb') as f:
            shutil.copyfileobj(raw, f)

    def deleteFile(self, path):
        if os.path.exists(path):
            os.remove(path)
            return True
        else:
            return False

    def ToFileTimeUtc(self, current=False):
        tick = (datetime.utcnow() - datetime(1, 1, 1)).total_seconds() * 10000000
        if current:
            return (datetime.now() - datetime(1, 1, 1)).total_seconds()
        if tick < 504911232000000000:
            raise
        return int(tick - 504911232000000000)
    
    def makeRandom(self):
        xyz = self.server.payloads['platform'] + "_" + self.server.payloads['channel'] + "_xyz"
        _xyz = '2|4|3|1|2'
        arr = _xyz.split('|')
        u = self.server.payloads['sdkUid'][int(len(self.server.payloads['sdkUid']) / int(arr[0])):]
        t = self.server.payloads['token'][int(len(self.server.payloads['token']) / int(arr[1])):]
        t2 = "{:%Y%m%d}".format(date.today()) #科普一下 %Y = 2019;%y = 19 記住的話世界會更美好
        #原本我以為是%y 干
        t3 = "{" + arr[2] + "}" + "{" + arr[3] + "}" + "{" + arr[4] + "}"
        t3 = t3.replace("{1}", u)
        t3 = t3.replace("{2}", t)
        t3 = t3.replace("{3}", t2)
        return hashlib.md5(t3.encode()).hexdigest()

BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

class AESCipher:

    def __init__(self, key):
        if type(key) != bytes:
            try:
                key = base64.b64decode(key)
            except:
                key = key.encode('utf8')
        if len(key) != 16:
            self.key = md5(key).hexdigest().encode("utf8")
        else:
             self.key = key

    def encrypt(self, raw):
        raw = pad(raw)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return base64.b64encode(cipher.encrypt(raw.encode("utf8")))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return unpad(cipher.decrypt(enc)).decode('utf8')