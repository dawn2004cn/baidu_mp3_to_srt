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
class shiwen():
    # 初始化函数
    def __init__(self):
        #self.huiben_type ={'guoneihuiben','guowaihuiben','guoxuezaojiao','kewenlangsong','shuiqiangushi','yingwenhuiben'}

        #self.huiben_type ={'guoneihuiben'}
        self.huiben_type = {'1014','575'}
        self.baseUrl1 = 'http://www.zgpingshu.com/play/567/'
        self.baseUrl = self.baseUrl1+'{}.html'
        self.name = '单田芳评书水浒传(上)'
        #self.firstUrl = 'https://www.youshenghuiben.com/{}'
        #self.soundUrl = "https://so.gushiwen.org/viewplay.aspx?id={}"
        self.file_path = f'.//'+self.name+'//'
        self.brower = webdriver.Chrome()
        if os.path.exists(self.file_path) == False:
            os.mkdir(self.file_path)
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
                   'Accept':'*/*'
                   }

    def __del__(self):
        print(f'__del__')
        #self.file.close()
        self.brower.close()

    #每个channel一个文件
    def open(self,channel):
        self.file = open(channel+".json", "a+",encoding='utf-8')

    #关闭文件
    def close(self):
        self.file.close()

    def getHtml(self,url):
        ''' 爬取网页数据 '''
        print(f"getHtml...{url}")
        self.headers['user-agent'] = random.choice(UA_LIST)
        html = requests.get(url, headers=self.headers)
        html.encoding = 'utf-8'
        text = html.text
        return text


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
    def getSound(self,url,name):
        print(f"sound url:{url}")
        #html = self.getHtml(url)

        self.brower.get(url)
        #print(self.brower.page_source)
        #more = brower.find_element_by_xpath('//div[@class="unfold-field_text"]/span')
        #more.click()
        wait = WebDriverWait(self.brower, 20)
        #element = wait.until(EC.presence_of_element_located((By.ID, 'jquery_jplayer_1')))
        element = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="jquery_jplayer_1"]/audio')))
        #element = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="jquery_jplayer_1"]/audio')))
        print(element)
        # 设定页面加载限制时间
        #self.brower.set_page_load_timeout(25)
        #return self.parseSoundUrl(html)

        player = self.brower.find_element_by_xpath('//div[@id="jquery_jplayer_1"]/audio')

        # print(jplayer)
        # print(player.find_element_by_xpath('./audio/@src'))
        print(player.get_attribute('src'))

        value = {}
        value['audio'] = player.get_attribute('src')
        audioname = os.path.basename(value['audio'])
        kname = str(name)
        audioname = self.name+"_"+kname.zfill(3)+".mp3"
        self.download(value['audio'], audioname)
        return value['audio']

    def parseSound(self):
        self.open(self.name)
        for value in range(1,181):
            huibenurl = self.baseUrl.format(value)
            if value == 1:
                huibenurl = self.baseUrl1
            #huibenHtml = self.getHtml(huibenurl)
            values = {}
            values['audio'] = self.getSound(huibenurl,value)
            kname = str(value)
            values['name'] = kname.zfill(3)
            self.file.write(str(values).encode('utf-8').decode('utf-8'))
            self.file.write(f'\n')
            #self.parseHtml(huibenHtml)
        self.close()
if __name__ == '__main__':
    shiwen = shiwen()
    shiwen.parseSound()
    #url = 'https://res.youshenghuiben.com/zb_users/upload/2020/01/huiben_20200114230734_11090.jpeg!lpic'
    #name =os.path.basename(url)
    #name = name[:-5]
    #print(name)
'''
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
import time

driver = webdriver.Chrome()
driver.get('https://www.youshenghuiben.com/guoneihuiben/woyaobanchuqu127.html')

# print(driver.page_source)
more = driver.find_element_by_xpath('//div[@class="unfold-field_text"]/span')
more.click()
containets = driver.find_elements_by_xpath('//div[@id="containet"]/ul[@id="pageMain"]/li')

# 设定页面加载限制时间
driver.set_page_load_timeout(10)

# print(containets.size)
for containet in containets:
    print(containet.text)

wait = WebDriverWait(driver, 30)
# element = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="btn btn-search"]')))

jplayers = driver.find_element_by_xpath(
    '//div[@id="jp_container_1"]/div[@class="jp-type-single"]/div[@class="jp-gui jp-interface"]/div[@class="jp-controls"]/button')
# jplayer.click()
# js = driver.execute_script("arguments[0].click();", jplayers)
# print(driver.execute_script('return document.getElementById("jquery_jplayer_1").innerText'))

# driver.executeScript("arguments[0].click();",jplayers);

print(driver.page_source)

player = driver.find_element_by_xpath('//div[@id="jquery_jplayer_1"]')

# print(jplayer)
print(player.find_element_by_xpath('./audio/@src'))

'''