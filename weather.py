# encoding=gbk
import re
import pinyin
import requests
import lxml.etree as etree

def getHtml(url):
    print(url)
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
               'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    html = requests.get(url, headers=headers)
    html.encoding = 'gbk'
    text = html.text
    return text


def getdata_total(html):
    tree = etree.HTML(html, parser=etree.HTMLParser(encoding='utf-8'))
    nodes = tree.xpath('//table[@class="t12"]/tr')
    for node in nodes:
        data_total = node.xpath('./td[1]/text()')
        data_total = "".join(data_total)
        print(data_total)

city_info = getHtml('http://pv.sohu.com/cityjson')
print(city_info)  # 看输出结构
'''var returnCitySN = {"cip": "119.137.1.150", "cid": "440300", "cname": "广东省深圳市"};'''
addr = city_info.split('=')[1].split(',')[2].split('"')[3]  # 取出地址信息
print(addr)

#汉字转换为不带声调的拼音
f = pinyin.get(addr,format='strip')
print(f)   # 看输出地址拼音结构
provice = f.split('sheng', 1)[0].replace(' ', '')  # 获取省份
print(provice)
city = f.split('shi')[0].split('sheng')[1].strip().replace(' ', '')  # 获取城市
print(city)
url = 'http://qq.ip138.com/weather/{}/{}.htm'.format(provice, city)
# 分析url可知某省某市的天气url即为上面格式
wea_info = getHtml(url)

getdata_total(wea_info)
tianqi_pattern = 'alt="(.+?)"'
tianqi = re.findall(tianqi_pattern, wea_info)  # 获取天气信息
print(tianqi)
wendu_pattern = '<td>([-]?\d{1,2}.+)</td>'
wendu = re.findall(wendu_pattern, wea_info)  # 获取温度信息
print(wendu)
wind_pattern = '<td>(\W+\d{1,2}.+)</td>'
wind = re.findall(wind_pattern, wea_info)  # 获取风向信息
print(wind)

print('位置：', addr)
print('天气：', tianqi[0])  # 当天天气，明天天气即为tianqi[1],最多获取6天天气
print('温度：', wendu[0])  # 当天温度
#print('风向：', wind[0])   # 当天风向
