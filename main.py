# 403 Foorbidden解決方法：https://blog.csdn.net/eric_sunah/article/details/11301873
# https://stackoverflow.com/questions/36076052/beautifulsoup-find-all-on-bs4-element-resultset-object-or-list
# https://stackoverflow.com/questions/5815747/beautifulsoup-getting-href
# 目標：搜索十頁大於50推的文章內容
from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup


def find_previous_website(bs):
    search_bar = bs.find("div", "action-bar")
    prev_url = search_bar.find_all("a")[3]["href"]
    ptt_website = "https://www.ptt.cc/"
    return ptt_website + prev_url


def crawl_website(bs):
    return_list = []
    # 最新的一面為16個文章，之前的為20個文章
    main_page = bs.find_all("div", "r-ent")
    for element in main_page:
        vote = element.find("span", "hl f3")
        title = element.find("div", "title")
        hyperlink = element.find("a")
        name = element.find("div", "author")
        date = element.find("div", "date")

        if vote is None:
            vote = 0
        elif type(vote) is not int:
            vote = vote.get_text()

        title = title.get_text()
        hyperlink = "http://www.ptt.cc" + hyperlink.get("href")
        name = name.get_text()
        date = date.get_text()

        # why title[1:-1] 的 -1會把\n消掉？
        buf = [vote, title[1:-1], hyperlink, name, date]
        return_list.append(buf)
    return return_list


output = open("result.txt", "w")
print("How many page you want to crawl?")
page = 1

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) \
Gecko/20100101 Firefox/23.0"}
req = Request(url="http://www.ptt.cc/bbs/FORMULA1/index.html", headers=headers)
html = urlopen(req).read()

bs = BeautifulSoup(html, "html.parser")
last_page = find_previous_website(bs)  # 找到前一頁
data_set = crawl_website(bs)  # 把目前的這一頁抓下來


# list 預設格式為 vote/title/href/name/date
for ele in data_set:
    print("Vote:", ele[0], file=output, sep="")
    print("Title:", ele[1], file=output, sep="")
    print("Hyperlink:", ele[2], file=output, sep="")
    print("Author:", ele[3], file=output, sep="")
    print("Date:", ele[4], file=output, sep="")
    print("\n", file=output)


output.close()
