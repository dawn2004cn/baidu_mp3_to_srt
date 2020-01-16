import importlib
import sys
importlib.reload(sys)
import requests
import lxml.etree as etree
import os

class shiwen():
    # 初始化函数
    def __init__(self):
        self.total_url = 'https://so.gushiwen.org'
        self.baseUrl = 'https://so.gushiwen.org/shiwen'
        self.soundUrl = "https://so.gushiwen.org/viewplay.aspx?id={}"
        self.file_path = f'.//sound//'
        if os.path.exists(self.file_path) == False:
            os.mkdir(self.file_path)
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
                   'Accept':'*/*'
                   }

    def __del__(self):
        print(f'__del__')
        #self.file.close()

    #每个channel一个文件
    def open(self,channel):
        self.file = open(channel+".json", "w",encoding='utf-8')

    #关闭文件
    def close(self):
        self.file.close()

    def getHtml(self,url):
        ''' 爬取网页数据 '''
        print(f"getHtml...{url}")
        html = requests.get(url, headers=self.headers)
        html.encoding = 'utf-8'
        text = html.text
        return text

    #解析html页
    #替换url中的变量，例如：https://so.gushiwen.org/shiwen/default_1Ab26259653a5dA{1}.aspx 中的channel
    def parsefirst(self,first_url,channel):
        url = first_url[:-6]+str(channel)+first_url[len(first_url)-5:]
        html = self.getHtml(url)
        self.parseHtml(html)

    #解析所有作者的作品以及url
    def parseAuthor(self):
        html = self.getHtml(self.baseUrl)
        if len(html) != 0:
            try:
                tree = etree.HTML(html, parser=etree.HTMLParser(encoding='utf-8'))
                nodes = tree.xpath('//div[@id="type2"]/div[@class="sright"]/a')
                id = 1
                values = []
                for node in nodes:
                    value = {}
                    author = node.xpath('./text()')
                    href = node.xpath('./@href')
                    value['author'] = "".join(author)
                    value['href'] = self.total_url+"".join(href)
                    values.append(value)
                return values
            except:
                print("fail")
            return ""

    #解析一页所有诗文数据 html页数据
    def parseHtml(self,html):
        if len(html) != 0:
            try:
                tree = etree.HTML(html, parser=etree.HTMLParser(encoding='utf-8'))
                nodes = tree.xpath('//div[@class="left"]/div[@class="sons"]')
                id = 1
                values = []
                for node in nodes:
                    value = {}
                    title = node.xpath('./div[@class="cont"]/p[1]/a/b/text()')
                    dynasty = node.xpath('./div[@class="cont"]/p[@class="source"]/a[1]/text()')
                    author = node.xpath('./div[@class="cont"]/p[@class="source"]/a[2]/text()')
                    contentnodes = node.xpath('./div[@class="cont"]/div[@class="contson"]')
                    for e in contentnodes:
                        content = e.xpath('string(.)')
                    soundid = node.xpath('./div[@class="tool"]/div[@class="shoucang"]/img/@id')

                    value['title'] = "".join(title)
                    value['dynasty'] = "".join(dynasty)
                    value['author'] = "".join(author)
                    value['content'] = "".join(content)
                    id = "".join(soundid)
                    value['soundid'] = id.replace("likeImg","")
                    value['soundurl'] = self.getSound(value['soundid'])
                    value['soundname'] = value['soundid']+".mp3"

                    self.file.write(str(value).encode('utf-8').decode('utf-8'))
                    self.file.write(f'\n')
                    values.append(value)
                return values
            except:
                print("fail")
            return ""


    #下载声音
    def download(self,link,filename):
        try:
            pic = requests.get(link,headers=self.headers)
            if pic.status_code == 200:
                with open(os.path.join(self.file_path) + os.sep + filename, 'wb') as fp:
                    fp.write(pic.content)
                    fp.close()
            print("下载完成")
        except Exception as e:
            print(e)

    #获取声音url
    def getSound(self,id):
        url = self.soundUrl.format(id)
        html = self.getHtml(url)
        return self.parseSoundUrl(id,html)

    def parseSoundUrl(self,id,html):
        if len(html) != 0:
            try:
                tree = etree.HTML(html, parser=etree.HTMLParser(encoding='utf-8'))
                nodes = tree.xpath('//div')
                #id = 1
                values = []
                for node in nodes:
                    value = {}
                    audio = node.xpath('./audio/@src')
                    value['audio'] = "".join(audio)

                    self.download(value['audio'],id+".mp3")
                return value['audio']
            except:
                print("fail")
            return ""


    def parseAll(self):
        values = self.parseAuthor()
        for value in values:
            self.open(value['author'])
            for i in range(1, 21):
                self.parsefirst(value['href'],i)
            self.close()

if __name__ == '__main__':
    shiwen = shiwen()
    shiwen.parseAll()
