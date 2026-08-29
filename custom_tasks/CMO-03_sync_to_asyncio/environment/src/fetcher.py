import time
def fetch(url):
    time.sleep(0.2)
    return 'ok'
def main(urls):
    return [fetch(u) for u in urls]
