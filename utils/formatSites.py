import json, os

filename = 'sites.json'
with open(filename, 'r') as f:
    data = json.load(f)

for site in data:
    s = site
    site = data[site]
    site['notifGroup'] = 'main'
    site['active'] = True
    site['url'] = s
    site['sendPassProds'] = False
    
os.remove(filename)
with open(filename, 'w') as f:
    json.dump(data, f, indent=4)