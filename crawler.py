"""
time: 2019.06.03 15:34
author: gao yang
"""

import requests
from Config import ExtractRules as Rule
from Config import stupidSpiderConfig as Config
from lxml import etree
from bs4 import BeautifulSoup
from piplines import OriginalWebContent, UrlListPipline, process_data, StupidSpiderPipline, article2file

SOGOU_URL = "http://www.sogou.com/web?query=" + Config.keyword + "+site%3A" + Config.url_list[0]
BAIDU_URL = "http://www.baidu.com/s?wd=" + Config.keyword + " site%3A" + Config.url_list[0]
GOOGLE_URL = "https://www.google.com/search?q=" + Config.keyword + "+site%3A" + Config.url_list[0]


def get_news_list(url):
    print("crawl website:{}".format(url))
    response = requests.get(url, headers=Config.User_headers)
    response.encoding = 'utf-8'

    html = etree.HTML(response.text, etree.HTMLParser())
    title = html.xpath('//title')[0].text

    OriginalWebContent({"title": title, "content": response.text})

    element_links = html.xpath(Rule.baidu_news_xpath['link'])
    print(element_links)
    links = [get_real_url(link) for link in element_links]
    # 保存到url_list.txt文件中
    UrlListPipline(links)


def get_real_url(url):
    response = requests.get(url, allow_redirects=False)
    real_url = response.headers.get('Location')

    return real_url

def get_content(url):
    response = requests.get(url, headers=Config.User_headers)
    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.title.string.strip()

    html = etree.HTML(response.text, etree.HTMLParser())
    time = html.xpath(Rule.nbd_com_cn_xpath['time'])[0].strip()
    print(title,"-",time)

    tags_content = html.xpath(Rule.nbd_com_cn_xpath['content'])[0]
    content = tags_content.xpath("string(.)").strip()

    data = {
        "title": title,
        "time": time,
        "content": content
    }
    StupidSpiderPipline(data)
    article2file(data)


if __name__ == "__main__":
    # get_news_list(BAIDU_URL)
    links = process_data()
    for link in links:
        print("crawl link: {}".format(link))
        get_content(link)
