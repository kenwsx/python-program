from urllib.request import urlopen
from urllib.request import Request
import json

output = open("api.txt", "w")

movie = input(
    "Please type the movie you want to search.\n(space use + to describe)")

# 以前的方法，用urlopen
req = Request(
    url=f"http://www.omdbapi.com/?t={movie}&apikey=3f856a29")
decode_json1 = urlopen(req).read().decode("utf-8")  # 這邊為json格式
decode_dic1 = json.loads(decode_json1)  # 轉換為dict格式
print("raw json file:", decode_json1, file=output)


if decode_dic1.get("Response") == "True":
    # 以dict而言，用[] 或者 .get有一樣的結果
    print("Title:", decode_dic1.get("Title"), file=output)
    print("Year:", decode_dic1.get("Year"), file=output)
    print("Rated:", decode_dic1.get("Rated"), file=output)
    print("Released:", decode_dic1.get("Released"), file=output)
    print("Ratings(IDMB):", decode_dic1.get(
        "Ratings")[0]["Value"], file=output)
else:
    print("No movie found!")
