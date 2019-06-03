"""
time: 2019.06.03 15:27
author:gao yang
"""


class StupidSpiderPipline():

    def __init__(self, data):
        with open("extract_data.csv", 'a+', encoding='utf-8') as f:
            f.writelines(data["title"] + "," + data['time'] + "," + data["content"])


class OriginalWebContent():

    def __init__(self, data):
        with open("news_data/" + data["title"].split("s")[0] + ".html", 'w+', ) as f:
            f.write(data["content"])


class UrlListPipline():
    def __init__(self, data):
        with open("url_list.txt", "w", encoding='utf-8') as f:
            f.writelines(url + "\n" for url in data)


def process_data():
    with open("url_list.txt", 'r', encoding="utf-8") as f:
        url_list = f.readlines()

    url_list = [url.strip() for url in url_list]
    return url_list


def article2file(data):
    with open("news_data/"+ data['title'] +".txt",'w+',encoding='utf-8') as f:
        f.writelines(data["title"] + "\n" + data['time'] + "\n" + data["content"])