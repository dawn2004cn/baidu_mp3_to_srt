import importlib
import sys
importlib.reload(sys)
import requests
import lxml.etree as etree
import os
import selenium as webdriver

UA_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
class shiwen():
    # 初始化函数
    def __init__(self):
        #self.huiben_type ={'guoneihuiben','guowaihuiben','guoxuezaojiao','kewenlangsong','shuiqiangushi','yingwenhuiben'}

        self.huiben_type ={'guoneihuiben'}
        self.baseUrl = 'https://www.youshenghuiben.com/{}/{}'
        self.firstUrl = 'https://www.youshenghuiben.com/{}'
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

    #解析一页所有诗文数据 html页数据
    def parseHtml(self,html):
        if len(html) != 0:
            try:
                tree = etree.HTML(html, parser=etree.HTMLParser(encoding='utf-8'))
                nodes = tree.xpath('//div[@class="border_gray"]/article[@class="archive-list"]')
                id = 1
                values = []
                for node in nodes:
                    value = {}
                    imgurl = node.xpath('./figure[@class="thumbnail"]/a/img/@src')
                    name = node.xpath('./header[@class="entry-header"]/h2[@class="entry-title"]/a/text()')
                    href = node.xpath('./header[@class="entry-header"]/h2[@class="entry-title"]/a/@href')
                    updatetime = node.xpath('./div[@class="entry-content"]/span[@class="entry-meta"]/span/text()')
                    desc = node.xpath('./div[@class="entry-content"]/div[@class="archive-content"]/text()')
                    tag  = node.xpath('./div[@class="entry-content"]/div[@class="archive-tag"]/a/text()')

                    value['imgurl'] = "".join(imgurl)
                    value['name'] = "".join(name)
                    value['href'] = "".join(href)
                    value['updatetime'] = "".join(updatetime)
                    value['desc'] = "".join(desc)
                    value['tag'] = "".join(tag)

                    #下载声音
                    #value["sound"] = self.getSound(value['href'])

                    imagename = os.path.basename(value['imgurl'])
                    value["imagename"] = imagename[:-5]
                    #下载图片
                    self.download(value['imgurl'],value["imagename"])

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
    def getSound(self,url):
        print(f"sound url:{url}")
        html = self.getHtml(url)
        return self.parseSoundUrl(html)

    def parseSoundUrl(self,html):
        if len(html) != 0:
            try:
                tree = etree.HTML(html, parser=etree.HTMLParser(encoding='utf-8'))
                nodes = tree.xpath('//div[@class="f1"]/span[@class="huibenzaixian"]')
                #id = 1
                value = {}
                for node in nodes:
                    audio = node.xpath('./div[@class="jquery_jplayer_1"]/audio/@src')
                    value['audio'] = "".join(audio)
                    audioname = os.path.basename(value['audio'])
                    self.download(value['audio'],audioname)
                return value['audio']
            except:
                print("fail")
            return ""

    def getTotalPage(self,html):
        if len(html) != 0:
            try:
                tree = etree.HTML(html, parser=etree.HTMLParser(encoding='utf-8'))
                nodes = tree.xpath('//nav[@class="navigation pagination"]/div[@class="nav-links"]')
                #id = 1
                values = []
                for node in nodes:
                    value = {}
                    href = node.xpath('./a[@title="最后一页"]/@href')
                    value['href'] = "".join(href)
                    url = value['href']
                    page = int(url[url.rindex('/')+1:])
                return page
            except:
                print("fail")
            return ""


    def parseAll(self):
        for value in self.huiben_type:
            self.open(value)
            url = self.firstUrl.format(value)
            html = self.getHtml(url)
            totalpage = self.getTotalPage(html)
            for i in range(1,totalpage):
                huibenurl = self.baseUrl.format(value,i)
                huibenHtml = self.getHtml(huibenurl)
                self.parseHtml(huibenHtml)
            self.close()

if __name__ == '__main__':
    shiwen = shiwen()
    shiwen.parseAll()
    #url = 'https://res.youshenghuiben.com/zb_users/upload/2020/01/huiben_20200114230734_11090.jpeg!lpic'
    #name =os.path.basename(url)
    #name = name[:-5]
    #print(name)
