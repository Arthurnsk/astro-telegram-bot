import requests
import time

def moon():
    try:
        url = "https://api.farmsense.net/v1/moonphases/?d=" + str(int(time.time()))
        r = requests.get(url, timeout=10)
        r.raise_for_status()

        data = r.json()

        if data:
            return data[0]["Phase"]

        return "неизвестная фаза луны"

    except requests.RequestException:
        return "активная фаза луны"
