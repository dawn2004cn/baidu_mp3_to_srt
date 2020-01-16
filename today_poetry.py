
import requests
import json

class today_poerty():
    def __init__(self):
        self.url = "https://v2.jinrishici.com/sentence"
        print("__init__")

    def __del__(self):
        print("__del__")

    def getHtml(self,url):
        print(url)
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
                   'Cookie':'X-User-Token=QnODCyj9vVCZv0BSxaTTwbIF+CXmVT1s'}
        html = requests.get(url, headers=headers)
        #html.encoding = 'gbk'
        text = html.text
        return text

    def getPoetry(self):
        html = self.getHtml(self.url)
        jobj = json.load(html)
        print(json)


if __name__ == '__main__':
    today = today_poerty()
    today.getPoetry()
#    house.parseHouse(huarun2)


