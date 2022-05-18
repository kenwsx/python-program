import requests
from bs4 import BeautifulSoup

s = requests.Session()

login_url = 'https://mox.moe/login.php'
username = 'ken205115331@gmail.com'
password = '91qaz6yhnA'
download_url = "https://mox.moe/down/10188/1006/0/2/1-0/"
file_name = "[Mox.moe][日常]卷06.kepub.epub"

payload = {'username': username,
           'password': password}

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

entry = s.post(login_url, headers=header, data=payload)
print(entry.status_code)

'''r = requests.get(download_url, allow_redirects=True)
with open(file_name, "wb") as f:

    f.write(r.content)'''

page = s.get("https://mox.moe/c/10188.htm")
print(page.text)
