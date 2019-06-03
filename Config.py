"""
time：2019.06.03
author：gao yang
"""


class stupidSpiderConfig(object):

    User_headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

    url_list = ["www.nbd.com.cn/"]
    keyword = "中美贸易战"


class ExtractRules(object):
    google_news_xpath = {
        "link": "//div[@class='g']/div/div/div/a/@href"
    }

    baidu_news_xpath = {
        "link": "//div[@id='content_left']/div/h3/a/@href",
    }

    sogou_news_xpath = {
        "link": "//div[@class='main']/div/div[@class='results']/div/h3/a/@href"
    }

    sina_com_xpath = {
        "title": "",
        "time": "",
        "content": ""
    }

    nbd_com_cn_xpath = {
        "title": "//title/text()",
        "time": "//div[@class='g-article']/div[@class='g-article-top']/p[@class='u-time']/span[@class='time']/text()",
        "content": "//div[@class='g-article']/div[@class='g-articl-text']"
    }
