import requests
import json
import pprint

apl = "https://api.openbd.jp/v1/get?isbn="

isbn = "9784088815564"


result = requests.get(apl + isbn)
res = result.json()

try:
  data = {
    "i" : res[0]["summary"]["isbn"],
    "t" : res[0]["summary"]["title"],
    "p" : res[0]["summary"]["publisher"],
    "a" : res[0]["summary"]["author"],
    "c" : res[0]["summary"]["cover"]
    }
  print(data)
except:
  print("エラーです")
  






