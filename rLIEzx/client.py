# -*- coding: utf-8 -*-
from .models import *
from .server import Server
from .lie import API
import time

class MYRZX(API, Models):
    isLogin = False
    
    def __init__(self, loginUserData):
        Models.__init__(self)
        self.server = Server(self)
        API.__init__(self)
        self.server.setHeadersWithDict({
            'User-Agent': 'Mozilla/5.0 (Android; U; zh-TW) AppleWebKit/533.19.4 (KHTML, like Gecko) AdobeAIR/32.0'
        })
        self.firstOpen()
        #self.loginFunplusgame(email, password)
        self.sdkLogin(loginUserData)
        if self.isLogin:
            self.__initAll()

    def __initAll(self):
        self.unlockStage = list(self.master['history']['unlockStage'])