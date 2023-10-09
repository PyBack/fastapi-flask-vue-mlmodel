import time
import requests

while True:
    requests.get('http://localhost:5500/ping')
    time.sleep(1)
