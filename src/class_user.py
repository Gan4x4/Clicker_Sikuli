'''
Created on 10.08.2013

@author: Anton
'''
#import class_browser
#reload(class_browser)
#from class_browser import *

class User():
    def __init__(self,login,password):
        #global Browser
        self.login = login
        self.password = password
        self.ip = []
        self.sites = []
        self.current_ip = 0
        #self.browser = Browser(login)
    def addIp(self,ip,port):
        self.ip.append({'ip':ip,'port':port})
    def getCurrentIp(self):
        if len(self.ip) == 0:
            return False
        return self.ip[self.current_ip]['ip']
    def getCurrentPort(self):
        return self.ip[self.current_ip]['port']
    def asseptIp(self,test_ip):
        for i in self.ip:
            if i['ip'] == test_ip:
                return True 
        return False
    def asseptSite(self,url):
        i = 0;
        found = False
        for s in self.sites:
            if not (url.find(s) == -1):
                i = i + 1
                found = s
        if i == 0:
            return False
        if i > 1:
            raise Exception("Bad name for site")
        else:
            return found
    def getIp(self,num):
        try:
            if not( num < len(self.ip)):
                return False
            return self.ip[num]
        except:
            return False


