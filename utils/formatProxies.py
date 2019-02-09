# Formats proxies from proxiesForYou format to ip:port:user:pass

with open('p4u.txt') as t:
    proxies = t.readlines()

newProxies = ""

for proxy in proxies:
    temp = proxy.split(" ")[0].replace(" ", "")
    newProxies += temp + "\n"

print(newProxies)
