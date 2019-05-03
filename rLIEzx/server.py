# -*- coding: utf-8 -*-
from .config import Config
from .models import *
import json, requests, urllib, hashlib, base64

class Server(Config):
    _session = requests.session()
    Headers = {}

    def __init__(self, client=None):
        self.client = client
        self.Headers = {}
        self.Crypter = AESCipher('O/UT+WpvDymb26pF485QOA==')
        self.reqid = 0
        self.reqsid = 0
        Config.__init__(self)

    def urlEncode(self, url, path, params=[]):
        return url + path + '?' + urllib.parse.urlencode(params)

    def getJson(self, url, allowHeader=False, Headers={}):
        if allowHeader is False:
            return json.loads(self._session.get(url).text)
        else:
            print(Headers)
            res = self._session.get(url, headers=Headers)
            print(res.status_code)
            return json.loads(res.text)

    def setHeadersWithDict(self, headersDict):
        self.Headers.update(headersDict)

    def setHeaders(self, argument, value):
        self.Headers[argument] = value

    def addHeaders(self, source):
        headerList={}
        headerList.update(self.Headers)
        headerList.update(source)
        return headerList

    def addPayload(self, source):
        payloadList={}
        payloadList.update(self.payloads)
        payloadList.update(source)
        return payloadList

    def optionsContent(self, url, data=None, headers=None):
        if headers is None:
            headers=self.Headers
        return self._session.options(url, headers=headers, data=data)

    def postContent(self, url, data=None, files=None, headers=None):
        if headers is None:
            headers=self.Headers
        return  self._session.post(url, headers=headers, data=data, files=files)

    def send(self, url, data={}, serverMode=1, decode=True):
        if serverMode == 0:
            url = self.CENTER_SERVER + url
        if serverMode == 1:
            url = self.SERVER + url
        if serverMode == 2:
            url = self.PAY_SERVER + url
        data['token'] = self.payloads['token']
        data['reqid'] = self.reqid + 1
        data['reqsid'] = self.reqid + 1
        self.reqid += 1
        data = self.aesEncode(json.dumps(data))
        if decode:
            res = self.aesDecode(self._session.post(url, headers=self.Headers, data=data).text)
            self.errCodes(res)
            return res
        return  self._session.post(url, headers=self.Headers, data=data)

    def getContent(self, url, headers=None):
        if headers is None:
            headers=self.Headers
        return self._session.get(url, headers=headers, stream=True)

    def deleteContent(self, url, data=None, headers=None):
        if headers is None:
            headers=self.Headers
        return self._session.delete(url, headers=headers, data=data)

    def putContent(self, url, data=None, headers=None):
        if headers is None:
            headers=self.Headers
        return self._session.put(url, headers=headers, data=data)
    
    def errCodes(self, res):
        errorCode = res.get("resCode", 0)
        if errorCode == 0:
            return True
        elif errorCode == 997:
            pass
        else:
            self.client.isLogin = False
        print("[ERROR]%s(%s)"%(res['resMsg'], errorCode))
        if not self.client.isLogin:
            raise Exception('err%s'%errorCode)

    def aesEncode(self, data):
        return self.Crypter.encrypt(data)
        
    def aesDecode(self, encData):
        return json.loads(self.Crypter.decrypt(encData))