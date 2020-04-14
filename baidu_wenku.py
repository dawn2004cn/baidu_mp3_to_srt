# -*- coding: utf-8 -*-
# *** 吾爱 17788210295
import requests
import re
from json import loads
import os
from tqdm import tqdm


class Baidu(object):
    def __init__(self):

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Mobile Safari/537.36'
        }
        self.rtcs_flag = '1'
        self.rtcs_ver = '3.1'
        self.base_url = 'http://wkrtcs.bdimg.com/rtcs/webapp'
        self.base_img = 'https://wkrtcs.bdimg.com/rtcs/image'
        self.flag = True
        self.cout = 1

    def get_info(self, url):
        try:
            r = requests.get(url, headers=self.headers).content.decode()
        except Exception:
            print('编码错误,切换编码!')
            r = requests.get(url, headers=self.headers).content.decode('gbk')
        self.bucketNum = re.findall('"bucketNum":(\d+),', r)[0]
        self.sign = re.findall('&sign=(.*?)&', r)[0]
        self.rsign = re.findall('"rsign":"(.*?)",', r)[0]
        self.md5sum = re.findall('&md5sum=(.*?)&', r)[0]
        self.page_list = re.findall('"rtcs_range_info":(.*),"rtcs_flow"', r)[0]
        self.page_count = re.findall('"rtcs_page_count":(.*?),', r)[0]
        self.firstpageurl = re.findall('data-firstpageurl="(.*?)"', r)[0].replace('amp;', '')
        try:
            self.name = re.findall('<title>(.*?)</title>', r)[0].strip()
        except Exception:
            self.name = '百度文库百度文库'
        if not os.path.exists(self.name):
            os.mkdir(self.name)
        self.path = self.name + '/'

    # 解析翻页参数
    def parse(self):
        print('页数:', self.page_count)
        page_dics = loads(self.page_list)
        if int(self.page_count) >= 4:
            self.get_first()
            pn = 2
            rn = 4
            while True:
                a = ''
                ranges = page_dics[pn - 1:pn + rn - 1]
                for r in tqdm(ranges):  # 进度条
                    a += r.get('range') + '_' if (r is not ranges[-1]) else r.get('range')
                    try:
                        self.get_pages(pn, rn, a)
                    except Exception:
                        print('解析错误')
                pn = pn + rn
                rn = 5
                if pn > int(self.page_count):
                    break
        else:
            self.get_first()
            a = ''
            pn = 2
            rn = 4
            ranges = page_dics[pn - 1:pn + rn - 1]
            for r in tqdm(ranges):
                a += r.get('range') + '_' if (r is not ranges[-1]) else r.get('range')
            try:
                self.get_pages(pn, rn, a)
            except Exception:
                pass

    # 翻页写入文本
    def get_pages(self, pn, rn, ranges):
        dic = {
            'bucketNum': self.bucketNum,
            'pn': pn,
            'rn': rn,
            'md5sum': self.md5sum,
            'sign': self.sign,
            'rtcs_flag': self.rtcs_flag,
            'rtcs_ver': self.rtcs_ver,
            'range': ranges,
            'rsign': self.rsign
        }
        page = requests.get(self.base_url, params=dic, headers=self.headers).text[5:-1]
        b = loads(page)
        a = ''
        for i in b['document.xml']:
            for m in i['c']:
                a += '\n'
                for n in m['c']:
                    try:
                        if isinstance(n['c'], str):
                            a += n['c']
                    except Exception:
                        pass
        with open(self.path + self.name + '.doc', 'a', encoding='utf-8') as f:
            f.write(a)

    # 解析第一页
    def get_first(self):
        print(self.firstpageurl)
        first_page = requests.get(url=self.firstpageurl, headers=self.headers).text[32:-1]
        b = loads(first_page)
        a = ''
        for i in tqdm(b['document.xml']):
            for m in i['c']:
                a += '\n'
                for n in m['c']:
                    try:
                        if isinstance(n['c'], str):
                            a += n['c']
                    except Exception:
                        pass
        with open(self.path + self.name + '.doc', 'a', encoding='utf-8') as f:
            f.write(a)
        print('第一页解析完成!!!')

    # 下载图片
    def down_img(self, cout, num):
        data = {
            'md5sum': self.md5sum,
            'sign': self.sign,
            'rtcs_ver': '3',
            'bucketNum': self.bucketNum,
            'ipr': '{"c":"word/media/image%s.png"}' % cout
        }

        data = requests.get(url=self.base_img, params=data)
        if data.status_code == 200:
            with open(self.path + str(num) + '.jpg', 'wb+') as f:
                f.write(data.content)
            print(self.name + '下载完成!')
        else:
            couts = str(cout) + '_1'
            print(couts)
            data = {
                'md5sum': self.md5sum,
                'sign': self.sign,
                'rtcs_ver': '3',
                'bucketNum': self.bucketNum,
                'ipr': '{"c":"word/media/image%s.png"}' % couts
            }
            data = requests.get(url=self.base_img, params=data)
            if data.status_code == 200:
                with open(self.path + str(num) + '.jpg', 'wb+') as f:
                    f.write(data.content)
                print(self.name + '下载完成!')
            else:

                self.flag = False

    def run(self, url):
        num = 0
        self.get_info(url)
        self.parse()
        print('页面写入完成!!!' + '-' * 20 + '下载图片>>>>>>')
        while self.flag:
            num += 1
            self.down_img(self.cout, num)
            self.cout += 1


if __name__ == '__main__':
    url = input('https://wenku.baidu.com/view/b3299351747f5acfa1c7aa00b52acfc789eb9f0e')
    b = Baidu()
    b.run(url)