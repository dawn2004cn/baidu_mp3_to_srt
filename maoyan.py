import importlib
import json
import sys

importlib.reload(sys)
import requests
from  requests.exceptions import RequestException
import lxml.etree as etree
import os
import re
from multiprocessing import pool


class maoyan():
    # 初始化函数
    def __init__(self):
        # self.channels = ["tv","movie","child","variety","cartoon","doco"]
        # self.channels = ["variety","cartoon","doco"]
        self.baseUrl = 'https://maoyan.com/board/4?offset={}'
        self.file_path = f'.//maoyan//'
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'
                        }

    def __del__(self):
        print(f'__del__')
        # self.file.close()

    # 每个channel一个文件
    def open(self, channel):
        self.file = open(channel + ".json", "w", encoding='utf-8')

    # 关闭文件
    def close(self):
        self.file.close()

    def getHtml(self, url):
        ''' 爬取网页数据 '''
        try:
            print(f"getHtml...{url}")
            html = requests.get(url, headers=self.headers)
            html.encoding = 'utf-8'
            if html.status_code == 200:
                text = html.text
                return text
            return None
        except RequestException:
            return None

    # 解析qq html页数据
    def parseHtml(self, html):
        print(html)
        if len(html) != 0:
            try:
                tree = etree.HTML(html, parser=etree.HTMLParser(encoding='utf-8'))
                nodes = tree.xpath('//dl[@class="board-wrapper"]/dd')
                id = 1
                values = []
                for node in nodes:
                    value = {}
                    index = node.xpath('./i/text()')
                    image = node.xpath('./a/img[@class="board-img"]/@data-src')
                    title = node.xpath('./div[@class="board-item-main"]/div[@class="board-item-content"]/div[@class="movie-item-info"]/p[@class="name"]/a/text()')
                    actor = node.xpath('./div[@class="board-item-main"]/div[@class="board-item-content"]/div[@class="movie-item-info"]/p[@class="star"]/text()')
                    time = node.xpath('./div[@class="board-item-main"]/div[@class="board-item-content"]/div[@class="movie-item-info"]/p[@class="releasetime"]/text()')
                    score = node.xpath('./div[@class="board-item-main"]/div[@class="board-item-content"]/div[@class="movie-item-number score-num"]/p[@class="score"]/i/text()')


                    value['index'] = "".join(index)
                    value['image'] = "".join(image)
                    value['title'] = "".join(title)
                    value['actor'] = "".join(actor).strip()[3:]
                    value['time'] = "".join(time).strip()[5:]
                    value['score'] = "".join(score)

                    self.file.write(str(value).encode('utf-8').decode('utf-8'))
                    self.file.write(f'\n')
                    values.append(value)
                return values
            except:
                print("fail")
            return ""

    def parse_one_page(self,html):
        pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                             +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                             +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
        items = re.findall(pattern,html)
        for item in items:
            yield {
                'index':item[0],
                'image':item[1],
                'title':item[2],
                'actor':item[3].strip()[3:],
                'time':item[4].strip()[5:],
                'score':item[5]+item[6]
            }
    def write_to_file(self,content):
        with open('result.txt','a',encoding='utf-8') as f:
            f.write(json.dumps(content,ensure_ascii=False)+'\n')
            f.close()

    def main(self,offset):
        url = self.baseUrl.format(offset)
        html = self.getHtml(url)
        for item in self.parse_one_page(html):
            print(item)
            self.write_to_file(item)

    def parseAll(self):
        self.open("maoyan")
        for i in range(10):
            html = self.getHtml(self.baseUrl.format(i*10))
            self.parseHtml(html)
        self.close()



if __name__ == '__main__':
    maoyan = maoyan()
    for i in range(10):
        maoyan.main(i*10)
    #maoyan.parseAll()

