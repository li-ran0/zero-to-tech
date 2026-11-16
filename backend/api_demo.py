import requests

resp = requests.get("https://httpbin.org/ip", timeout=10)
print(resp.json())
