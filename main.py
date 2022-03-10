from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import re

output_file = open("output.txt", "w")

try:
    html = urlopen("https://pythonscraping.com/pages/page3.html")
except HTTPError as e:
    print(e)
except URLError as e:
    print(e)
else:
    bs = BeautifulSoup(html, "html.parser")
    images = bs.find_all(
        "img", {"src": re.compile("\.\.\/img\/gifts\/img.*\.jpg")})
    # for image in images:
    #     print(image["src"], file=output_file)
    print(images, file=output_file)
output_file.close()
