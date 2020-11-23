import datetime

def unix_timestamp(timestamp=None):
    if timestamp is None:
        timestamp = datetime.datetime.utcnow()
    return int((timestamp - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)

def getval(d, key, default=None):
    d, s = getdict(d, key)
    return d.get(s, default)

def getdict(d, key):
    spl = key.split('.')
    for i in range(0, len(spl) - 1):
        d = d[spl[i]]
    return d, spl[-1]
