import importlib
import sys
importlib.reload(sys)
import requests
import lxml.etree as etree
import os

class v_qq():
    # 初始化函数
    def __init__(self):
        #self.channels = ["tv","movie","child","variety","cartoon","doco"]
        self.channels = ["variety","cartoon","doco"]
        self.baseUrl = 'https://v.qq.com/channel/child?_all=1&listpage=1&sort=18&channel={}'
        self.nextUrl = "https://v.qq.com/x/bu/pagesheet/list?_all=1&append=1&channel={}&listpage=2&pagesize=30&sort=18&offset={}"
        self.file_path = f'.//pic//'
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
                   'Accept':'*/*'
                   }
        self.data_float_url = 'https://node.video.qq.com/x/api/float_vinfo2?cid='

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
    def parsefirst(self,channel):
        url = self.baseUrl.format(channel)
        html = self.getHtml(url)
        self.getdata_total(html)
        self.parseHtml(html)

    def getdata_total(self,html):
        tree = etree.HTML(html, parser=etree.HTMLParser(encoding='utf-8'))
        nodes = tree.xpath('//div[@class="mod_list_filter"]')
        for node in nodes:
            data_total = node.xpath('./div/@data-total')
            pagemax = node.xpath('./div/@data-pagemax')
            self.data_total = "".join(data_total)
            self.pagemax = "".join(pagemax)
            print(data_total)
            print(pagemax)
        return data_total

    def parseLeft(self,channel):
        if self.data_total.isdigit():
            data_total = int(self.data_total)
        else:
            data_total = 5000
        for i in range(30,data_total,30):
            url =self.nextUrl.format(channel,i)
            print(url)
            html = self.getHtml(url)
            self.parseHtml(html)

    #解析qq html页数据
    def parseHtml(self,html):
        if len(html) != 0:
            try:
                tree = etree.HTML(html, parser=etree.HTMLParser(encoding='utf-8'))
                nodes = tree.xpath('//div[@class="list_item"]')
                id = 1
                values = []
                for node in nodes:
                    value = {}
                    figure_caption = node.xpath('./a/div[@class="figure_caption"]/text()')
                    videourl = node.xpath('./div[@class="figure_detail figure_detail_two_row"]/a/@href')
                    name = node.xpath('./div[@class="figure_detail figure_detail_two_row"]/a/text()')
                    desc = node.xpath('./div[@class="figure_detail figure_detail_two_row"]/div[@class="figure_desc"]/text()')
                    picurl = node.xpath('./a/img/@src')
                    data_float = node.xpath('./a/@data-float')

                    value['figure_caption'] = "".join(figure_caption)
                    value['videourl'] = "".join(videourl)
                    value['name'] = "".join(name)
                    value['desc'] = "".join(desc)

                    value['picurl'] = "http:"+"".join(picurl)
                    value['pic_name']= str(abs(hash(value['picurl'])))+'.jpg'
                    value['data_float'] = self.data_float_url+"".join(data_float)

                    #获取详情json数据
                    #value['data_float_result'] = self.get_card(value['data_float'])

                    self.file.write(str(value).encode('utf-8').decode('utf-8'))
                    self.file.write(f'\n')
                    #self.download(value['picurl'],value['pic_name'])
                    values.append(value)
                return values
            except:
                print("fail")
            return ""


    #获取视频详情页json数据
    def get_card(self,data_float):
        html = self.getHtml(data_float)
        return html

    #下载图片
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

    def parseAll(self):
        for channel in self.channels:
            self.open(channel)
            self.parsefirst(channel)
            self.parseLeft(channel)
            self.close()

    def get_all_data_total(self):
        for channel in self.channels:
            url = self.baseUrl.format(channel)
            html = self.getHtml(url)
            data_total = self.getdata_total(html)
            print(data_total)

if __name__ == '__main__':
    v_qq = v_qq()
    v_qq.parseAll()
