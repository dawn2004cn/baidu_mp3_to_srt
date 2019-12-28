import importlib
import sys
from datetime import time

importlib.reload(sys)
import requests
import json
import os
import urllib
import schedule
import time;


class XiaoyaOS():
    # 初始化函数
    def __init__(self,albumId,name):
        # 定义初始的文件路径，需要拼接
        # 定义将数据写入到test.txt文件
        self.albumId = albumId
        self.name = name
        self.path = ".\\xiaoya\\"
        self.sigtext = {"appKey":"","appSecret":"","deviceId":"","sn":""}
        print(f"self.albumId:{self.albumId},self.name:{self.name}")
        self.detailUrl = f"http://api.ximalaya.com/ximalayaos-picture-book/api/content/getAudio?albumId={self.albumId}&name={name}&deviceId=18F0E416C676_9e6380f46382b857&appKey=70eefc246e3c4c749cb7c84d18859d4a&sn=11264_00_100264&sig=10163dd04c586096e5034a946c951f97"


    #获取html txt
    def getHouseHtml(self,url):
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
            'Connection':'close'
        }
        try:
            html = requests.get(url,headers=headers)
            text = html.text
        except:
            time.sleep(5)
        return text

    '''
    1、{"msg": "success", "code": 0, 
    "info": {"id": "c3b7cec7976aa10b9ca96cdcc343cbfb", 
    "name": "3",
    "audioUrl": "http://ximalayaos.cos.xmcdn.com/storages/90c2-ximalayaos/0D/18/CMCoCqUBwUcqAASQdgAGOqpj.mp3?sign=1577174684-uhy1vywzo-0-99d76e5fa28d4b4a27f0cab38ca8596b",
    "duration": 18}}
    2、{"msg":"未查询到单曲","code":10001}
    '''
    #解析房屋url数据
    def parseXiaoya(self):
        html = self.getHouseHtml(self.detailUrl)
        print(html)
        result = json.loads(html)
        print(result['code'])
        if result['code'] == 0:
            print(result['info']['audioUrl'])
            self.downloadAudio(result['info']['audioUrl'])
            return 0
        return 1

    def downloadAudio(self,url):
        path = f'{self.path}{self.albumId}\\'
        if os.path.exists(path):
            ""
        else:
            os.mkdir(path)
        name = url[0:url.find('?')]
        filename = os.path.basename(name)
        filePath = f"{path}{filename}"
        r = requests.get(url)
        with open(filePath, "wb") as code:
            code.write(r.content)


xiaoya = 'http://api.ximalaya.com/ximalayaos-picture-book/api/content/getAudio?albumId=06937&name=5&deviceId=18F0E416C676_9e6380f46382b857&appKey=70eefc246e3c4c749cb7c84d18859d4a&sn=11264_00_100264&sig=10163dd04c586096e5034a946c951f97'

def timer(n):
    '''''
    每n秒执行一次
    '''
    while True:
        print(time.strftime('%Y-%m-%d %X',time.localtime()))
        time.sleep(n)

if __name__ == '__main__':
    for i in range(10,12):
        for name in range(1,40):
            num = str(i)
            album = num.zfill(5)
            print(f'{album}\n')
            house = XiaoyaOS(album, name)
            if house.parseXiaoya() == 1:
                break
            time.sleep(5)