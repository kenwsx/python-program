from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup

try:
    html = urlopen("https://24h.pchome.com.tw/store/DYAJBQ")
except HTTPError as e:
    print(e)
except URLError as e:
    print(e)
else:
    bs = BeautifulSoup(html.read(), "html.parser")
    print(bs.h1)
