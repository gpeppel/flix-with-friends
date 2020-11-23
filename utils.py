import datetime

def unix_timestamp(timestamp=None):
    if timestamp is None:
        timestamp = datetime.datetime.utcnow()
    return int((timestamp - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
