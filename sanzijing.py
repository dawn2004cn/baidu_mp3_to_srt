import importlib
import sys

importlib.reload(sys)
import requests
import lxml.etree as etree
import pandas as pd
import openpyxl
import os
import shutil

detailUrl = 'https://www.sanzijing.org/{}.html'


class HouseToTxt():
    # 初始化函数
    def __init__(self):
        # 定义初始的文件路径，需要拼接
        self.detailUrl = "https://www.sanzijing.org/{}.html"
        # 定义将数据写入到test.txt文件
        self.file = open("sanzijing.txt", "w",encoding='utf-8')

    # 析构函数
    def __del__(self):
        self.file.close()
        print(f'__del__:{self.detailUrl}')

    def opencsv(self):
        self.file = open(self.building_file, "w", encoding='utf-8')

    def closecsv(self):
        self.file.close()

    # 获取html txt
    def getHouseHtml(self, url):
        html = requests.get(url)
        html.encoding = 'GBK'
        text = html.text
        return text

    # 解析房屋url数据
    def parseHouse(self, url):
        html = self.getHouseHtml(url)
        print(html)
        tree = etree.HTML(html, parser=etree.HTMLParser(encoding='utf-8'))
        value = {}
        tables = tree.xpath('//div/div[@class="STYLE4"]/table/tbody/tr/td/div/text()')
        for table in tables:
            tt = "".join(table)
            tt = tt.replace(u'\r\n', '').strip() + '\n'
            self.file.write(tt.encode('utf-8').decode('utf-8'))
        tables = tree.xpath('//div/div[@class="STYLE4"]/table/tbody/tr/td/div/*/text()')
        for table in tables:
            tt = "".join(table)
            tt = tt.replace(u'\r\n', '').strip() + '\n'
            self.file.write(tt.encode('utf-8').decode('utf-8'))
        nodes = tree.xpath('//div/div[@class="STYLE4"]/p/text()')
        for node in nodes:
            tt = "".join(node)
            tt = tt.replace(u'\r\n', '').strip() + '\n'
            self.file.write(tt.encode('utf-8').decode('utf-8'))


if __name__ == '__main__':
    house = HouseToTxt()
    for channel in range(1,124):
        tt = str(channel)+'\n'
        house.file.write(tt.encode('utf-8').decode('utf-8'))
        url = house.detailUrl.format(channel)
        house.parseHouse(url)

