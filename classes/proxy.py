from random import choice
from threading import Lock

from classes.logger import log

lock = Lock()

class Proxy:
    def __init__(self, proxyPath="./config/proxies.txt", useProxies=True):
        self.proxies = []

        self.currentProxy = 0

        self.useProxies = useProxies

        try:
            with open(proxyPath) as pf:
                for proxy in pf.readlines():
                    self.format(proxy.replace("\n", ""))
        except:
            log("[Error] - Unable to load proxies from file. Please check " + proxyPath)

        

    def format(self, proxyStr):
        proxyTemp = proxyStr.split(':')

        if len(proxyTemp) == 4:
            formatted = '{}:{}:{}@{}'.format(proxyTemp[2], proxyTemp[3], proxyTemp[0], proxyTemp[1])
        else:
            formatted = proxyTemp[0] + ':' + proxyTemp[1]
        
        self.proxies.append({
            'http': 'http://' + formatted,
            'https': 'https://' + formatted
        })

    def randomProxy(self):
        if self.useProxies:
            return choice(self.proxies)
        return False

    def nextProxy(self):
        if self.currentProxy >= len(self.proxies):
            self.currentProxy = 0
        
        self.currentProxy += 1

        with lock:
            if self.useProxies:
                return self.proxies[self.currentProxy]
            return False
        
    

