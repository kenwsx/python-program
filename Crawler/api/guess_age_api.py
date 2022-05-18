from urllib.request import urlopen
from urllib.request import Request
import json
import requests

output = open("api.txt", "w")

name = input("Please type your name.")

# 以前的方法，用urlopen
req = Request(url=f"https://api.agify.io?name={name}")
decode_json1 = urlopen(req).read().decode("utf-8")  # 這邊為json格式
decode_dic1 = json.loads(decode_json1)  # 轉換為dict格式
print("First method:", decode_json1, file=output)
# 以dict而言，用[] 或者 .get有一樣的結果
print("age:", decode_dic1.get("age"), file=output)


# 沒加.json()會印出回應結果，比如說這邊是Response 200，代表成功
req2 = requests.get(   # 轉換requests.models.Response->dict格式
    url=f"https://api.agify.io?name={name}").json()
print("Second method:", req2, file=output)
print("age:", req2["age"], file=output)
