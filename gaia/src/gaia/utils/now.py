import datetime

def now():
    'return a nano-second timestamp string'
    return datetime.datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S_%f')
