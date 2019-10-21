import time


def current_milli_time():
    return int(round(time.time() * 1000))


def old_api_version(data):
    return 'version' not in data or data['version'] != "2"