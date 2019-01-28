from datetime import datetime, timedelta

def timeParser(t):
    ret = datetime.strptime(t[0:19],'%Y-%m-%dT%H:%M:%S')
    if t[19]=='-':
        ret-=timedelta(hours=int(t[19:22]),minutes=int(t[23:]))
    elif t[19]=='+':
        ret-=timedelta(hours=int(t[19:22]),minutes=int(t[23:]))
    return ret