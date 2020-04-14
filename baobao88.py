import importlib
import random
import sys
importlib.reload(sys)
import requests
import lxml.etree as etree
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

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
class v_baobao():
    # 初始化函数
    def __init__(self):
        #self.channels = ["tv","movie","child","variety","cartoon","doco"]
        self.channels = ["index.html","index_2.html","index_4.html","index_3.html",
                         "index_guoxue.html","index_english.html","index_ps.html","index_yuer.html"]
        #self.channels = ["child"]
        self.baseUrl = 'http://www.baobao88.com/lianbo/'
        self.file_path = f'.//baobao88//'
        self.file_json = f'.//json//'
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
                   'Accept':'*/*'
                   }
        self.data_float_url = 'https://node.video.qq.com/x/api/float_vinfo2?cid='

        self.brower = webdriver.chrome()

    def __del__(self):
        print(f'__del__')
        self.brower.close()
        #self.file.close()

    #每个channel一个文件
    def open(self,channel):
        self.file = open(os.path.join(self.file_json) + os.sep+channel+".json", "w",encoding='utf-8')

    #关闭文件
    def close(self):
        self.file.close()

    def getHtml(self,url):
        ''' 爬取网页数据 '''
        print(f"getHtml...{url}")
        self.headers['user-agent'] = random.choice(UA_LIST)
        html = requests.get(url, headers=self.headers)
        html.encoding = 'gb2312'
        text = html.text
        return text

    def parseZhuanjiList(self, html):
        if len(html) != 0:
            try:
                tree = etree.HTML(html, parser=etree.HTMLParser(encoding='utf-8'))
                nodes = tree.xpath('//div[@class="faq"]/ul/li[@class="zjlist"]')
                id = 1
                values = []
                for node in nodes:
                    value = {}
                    zhuanji_name = node.xpath('./a/span/text()')
                    zhuanji_index_url = node.xpath('./a/@href')
                    zhuanji_pic_url = node.xpath('./a/img/@src')
                    zhuanji_pic_name = node.xpath('./a/img/@alt')

                    value['zhuanji_name'] = ("".join(zhuanji_name))
                    value['zhuanji_index_url'] = self.baseUrl+"".join(zhuanji_index_url)
                    value['zhuanji_pic_url'] = "".join(zhuanji_pic_url)
                    value['zhuanji_pic_name'] = ("".join(zhuanji_pic_name)+'.jpg')

                    self.zhuanji_name = value['zhuanji_name']
                    self.zhuanji_index_url = value['zhuanji_index_url']
                    self.zhuanji_pic_url = value['zhuanji_pic_url']
                    self.zhuanji_pic_name = value['zhuanji_pic_name']

                    self.download(value['zhuanji_pic_url'], value['zhuanji_pic_name'])
                    value['data'] = self.parseZhuanUrl(value['zhuanji_index_url'])


                    values.append(value)
                return values
            except Exception as e:
                print(e)
                print("fail")
            return ""
    def parseZhuanUrl(self,url):
        html = self.getHtml(url)
        if len(html) != 0:
            try:
                tree = etree.HTML(html, parser=etree.HTMLParser(encoding='utf-8'))
                nodes = tree.xpath('//div[@id="List"]/form/ul/li')
                id = 1
                values = []
                for node in nodes:
                    value = {}
                    song_name = node.xpath('./span[@class="songname"]/a/text()')
                    song_index_url = node.xpath('./span[@class="songname"]/a/@href')

                    value['song_name'] = ("".join(song_name))
                    value['song_index_url'] = "".join(song_index_url)
                    if len(value['song_index_url']) !=0:
                        sond_mp3 = self.getMp3(value['song_index_url'])
                        value['audio']=sond_mp3['audio']
                        value['sound_name'] = os.path.basename(sond_mp3['audio'])

                        value['zhuanji_name']= self.zhuanji_name
                        value['zhuanji_index_url'] = self.zhuanji_index_url
                        value['zhuanji_pic_url'] =self.zhuanji_pic_url
                        value['zhuanji_pic_name'] =self.zhuanji_pic_name
                        value['mp3_info'] = sond_mp3['mp3_info']
                        self.file.write(str(value).encode('utf-8').decode('utf-8'))
                        self.file.write(f'\n')
                        values.append(value)
                return values
            except Exception as e:
                print(e)
                print("fail")

            return ""

    def getMp3(self,url):
        print(f"sound url:{url}")

        self.brower.get(url)
        #print(self.brower.page_source)
        # more = brower.find_element_by_xpath('//div[@class="unfold-field_text"]/span')
        # more.click()
        # 设定页面加载限制时间
        self.brower.set_page_load_timeout(10)

        player = self.brower.find_element_by_xpath('//div[@id="jquery_jplayer_1"]/audio')

        mp3_info = self.brower.find_element_by_xpath('//div[@class="t_mp3_info t_mp3_gc"]')

        # print(jplayer)
        # print(player.find_element_by_xpath('./audio/@src'))
        print(player.get_attribute('src'))

        value = {}
        value['audio'] = player.get_attribute('src')
        value['mp3_info'] = mp3_info.text
        audioname = os.path.basename(value['audio'])
        self.download(value['audio'], audioname)
        return value

    #下载图片
    def download(self,link,filename):
        try:
            if not os.path.exists(self.file_path):
                os.mkdir(self.file_path)
            pic = requests.get(link,headers=self.headers)
            if pic.status_code == 200:
                with open(os.path.join(self.file_path) + os.sep + filename, 'wb') as fp:
                    fp.write(pic.content)
                    fp.close()
            print("下载完成")
        except Exception as e:
            print(e)

    def parseAll(self):
        for channel in self.channels:
            self.open(channel)
            url = self.baseUrl+channel
            html = self.getHtml(url)
            self.parseZhuanjiList(html)
            self.close()

if __name__ == '__main__':
    v_qq = v_baobao()
    v_qq.parseAll()
