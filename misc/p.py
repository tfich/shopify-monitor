

mainFile = open("site.txt",'r')
allSites = mainFile.readlines()
mainFile.close()

i = {}

from getSiteInfo import getSiteInfo
import time, json

for x in allSites:
    x = x.replace("\n", "")
    p = getSiteInfo(x)
    i[x]= p
    print(x)
    time.sleep(5)

print(json.dumps(i))