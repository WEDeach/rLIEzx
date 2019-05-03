# -*- coding: utf-8 -*-
from random import randint
import json, time, os, traceback, hashlib, urllib, base64
from Crypto import Random

def loggedIn(func):
    def checkLogin(*args, **kwargs):
        if args[0].isLogin:
            return func(*args, **kwargs)
        else:
            print('Login failed')
    return checkLogin

class User(object):

    def __init__(self):
        pass

    def loginFunplusgame(self, email, password):
        url = 'https://passport.funplusgame.com/client_api.php?ver=3'
        payloads = {
            'l': 'zh',
            'email': email,
            'password': password,
            'game_id': 20010,
            'method': 'signin',
            'origin_guid': origin_guid,
            'android_id': android_id
        }
        data = urllib.parse.urlencode(payloads)
        headers = {
            "Authorization": "FP 20010:" + authToken
        }
        r = self.server.postContent(url, headers=headers, data=data)
        print(r.text)
    
    def sdkLogin(self, encData):
        self.server.payloads = self.server.aesDecode(encData)
        r = self.server.send("userServerService/loginUser", self.server.payloads, 0)
        if r['playerInfo']['token'] != None:
            self.server.payloads['token'] = r['playerInfo']['token']
            self.isLogin = True
            self.server.serverId = r['servers'][0]['id']
            if self.selectServer(self.server.serverId):
                self.synchroTime()
                self.masterInfo = self.loadMasterInfo()["masterInfo"]
                self.master = self.loadMaster()
                self.master['data2'] = self.loadMaster2()
                print('[INFO]登入成功: ', self.masterInfo["roleName"])
    
    def firstOpen(self):
        payloads = {
            "os": "android",
            "osType": "android",
            "phoneScreen": "720*1280",
            "phoneFactory": "lge",
            "phoneModel": "LGM-V300K",
            "channel": "FUNPLUS",
            "isp": "\"WiredSSID\"",
            "network": "WIFI",
            "deviceId": "test",
            "imei": "unknow"
        }
        payloads['tjChannel'] = "tjDYD"
        r = self.server.send("userServerService/firstOpenGame", payloads, 0)
        print(r)

    @loggedIn
    def selectServer(self, serverId):
        np = {
            "random": self.makeRandom(),
            "isp": self.server.payloads['isp'],
            "deviceId": self.server.payloads['deviceId'],
            "tjChannel": self.server.payloads['tjChannel'],
            "imei": self.server.payloads['imei'],
            "osType": self.server.payloads['osType'],
            "serverId": serverId,
            "network": self.server.payloads['network']
        }
        r = self.server.send("userServerService/enterGame", np, 0)
        if self.isLogin:
            return True
        return False

class Acti(object):

    def __init__(self):
        pass
        
    @loggedIn
    def weekTaskFinish(self):
        return self.server.send("weekActivityService/getWeekActivityReward", {})

    @loggedIn
    def weekTaskInfo(self):
        return self.server.send("weekActivityService/queryWeekActivityInfo", {})

    @loggedIn
    def dailyGiftCheck(self):
        return self.server.send("dailyGiftService/dailyGiftSign", {})

    @loggedIn
    def updateDailyGift(self):
        return self.server.send("dailyGiftService/dailyGiftUpdate", {})

    @loggedIn
    def vipDailyGiftCheck(self):
        return self.server.send("vipService/getReward", {})

    @loggedIn
    def dailyCheckCheck(self):
        return self.server.send("dailyCheckService/dailyCheck", {})

class Battle(object):

    def __init__(self):
        pass
        
    @loggedIn
    def startBattle(self, id, battleType='stage', level=1):
        para = {
            "battleType": battleType
        }
        if battleType == 'stage':
            para['stageTypeId'] = id
            para['stageLevel'] = level
        else:
            para['taskTypeId'] = id
        return self.server.send("battleService/battleStart", para)

    @loggedIn
    def battleResult(self, stageId, win=True):
        #Nani the fuck win?? lollllllllllll*n
        para = {
            "stageId": stageId,
            "cityId": stageId[1],
            "result": int(win)
        }
        if win:
            self.unlockStage.append(stageId)
        return self.server.send("battleService/recordBattleResult", para)

class Gacha(object):

    def __init__(self):
        pass
    
    @loggedIn
    def timeEggGacha(self):
        return self.server.send("gachaService/gachaTimeEgg", {})

    @loggedIn
    def timeEggBuy(self, timeEggId):
        return self.server.send("mailService/mailQuery")

    @loggedIn
    def gacha(self, gachaId, num, voucherNum=0):
        if num < 1 or num > 50 or voucherNum <0 or voucherNum > 50:
            print('[INFO]數值限制@@...')
            return False
        return self.server.send("gachaService/gachaGetEggs", {
            "id": gachaId,
            "num": num,
            "voucherNum": voucherNum,
            "traceInfo": traceInfo
        })

class Mail(object):

    def __init__(self):
        pass
    
    @loggedIn
    def readMail(self, ids):
        para = {
            "mailIds": ids
        }
        return self.server.send("mailService/mailRead", para)

    @loggedIn
    def checkNew(self):
        return self.server.send("mailService/mailQuery")

    @loggedIn
    def deleteMail(self, mailIds):
        return self.server.send("mailService/mailBatchDel", {
            "mailIds": mailIds
        })

    @loggedIn
    def getReward(self, mailId):
        return self.server.send("mailService/mailGetReward", {
            "mailId": mailId
        })

class Master(object):

    def __init__(self):
        pass
    
    @loggedIn
    def createMaster(self, name, avatar=1):
        para = {
            "roleName": name,
            "serverId": self.server.serverId,
            "avatar": avatar
        }
        para['tjChannel'] = self.server.payloads['tjChannel']
        para['random'] = '3d5aa7b894b5ca3a05ba5aed2e548478'
        return self.server.send("userServerService/createMaster", para, 0)

    @loggedIn
    def loadMasterInfo(self):
        return self.server.send("masterService/masterQuery")

    @loggedIn
    def loadMaster(self):
        return self.server.send("masterService/masterQueryDetail")

    @loggedIn
    def loadMaster2(self):
        #lol func name
        return self.server.send("masterService/queryMasterSecondDetail")

    @loggedIn
    def checkTi(self):
        #確認時間? maybe "check time"
        return self.server.send("masterService/masterCheckTiAdd")

    @loggedIn
    def checkLevel(self):
        return self.server.send("masterService/masterLevelUpdate")

    @loggedIn
    def updateGuide(self, guide, isMain):
        return self.server.send("guideService/guideUpdate", {
            "tag": guide,
            "isMain": isMain
        })

    @loggedIn
    def getAvatar(self):
        return self.server.send("masterService/queryRoleAvatars")

    @loggedIn
    def setAvatar(self, avatar):
        return self.server.send("masterService/updateMasterAvatar", {
            "avatar": avatar
        })

    @loggedIn
    def changeName(self, newName):
        return self.server.send("masterService/masterNameUpdate", {
            "newName": newName
        })

class System(object):

    def __init__(self):
        pass
    
    @loggedIn
    def getNotice(self):
        return self.server.send("gameService/queryGameNotice", {})

    @loggedIn
    def synchroTime(self):
        return self.server.send("getSysCurTime/execute", {})

class RandomEvent(object):

    def __init__(self):
        pass
    
    @loggedIn
    def getFarmEvent(self):
        return self.server.send("gameEventService/getFarmEvent", {})

    @loggedIn
    def finishFarmEvent(self):
        return self.server.send("gameEventService/finishFarmEvent", {})

class Task(object):

    def __init__(self):
        pass

    @loggedIn
    def getTask(self, taskTypeId):
        return self.server.send("taskService/taskReceive", {
            "taskTypeId": taskTypeId
        })

    @loggedIn
    def finishStep(self, taskId, taskTypeId, removeIds, battleData=None):
        para = {
            "taskId": taskId,
            "removeIds": removeIds,
            "taskTypeId": taskTypeId
        }
        if battleData != None:
            para['battleData'] = battleData
        return self.server.send("taskService/taskCompleteStep", para)

    @loggedIn
    def finishTask(self, taskId, taskTypeId):
        return self.server.send("taskService/taskComplete", {
            "taskId": taskId,
            "taskTypeId": taskTypeId
        })

    @loggedIn
    def getLoopTask(self, taskTypeId, city):
        return self.server.send("taskService/taskLoopReceive", {
            "taskTypeId": taskTypeId,
            "city": city
        })

    @loggedIn
    def updateTask(self, unlockTasks, receiveTasks, removeTasks):
        return self.server.send("taskService/taskUpdate", {
            "unlockTasks": unlockTasks,
            "receiveTasks": receiveTasks,
            "removeTasks": removeTasks
        })

class API(User, Acti, Battle, Gacha, Mail, Master, System, RandomEvent, Task):
    def __init__(self):
        User.__init__(self)
        Acti.__init__(self)
        Battle.__init__(self)
        Gacha.__init__(self)
        Mail.__init__(self)
        Master.__init__(self)
        System.__init__(self)
        RandomEvent.__init__(self)
        Task.__init__(self)