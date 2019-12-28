import importlib
import sys
importlib.reload(sys)
import requests
import lxml.etree as etree


#detailUrl = 'http://ris.szpl.gov.cn/bol/'

detailUrl = 'http://zjj.sz.gov.cn/ris/bol/szfdc/'
class HouseToTxt():
    # 初始化函数
    def __init__(self):
        # 定义初始的文件路径，需要拼接
        self.detailUrl = "http://zjj.sz.gov.cn/ris/bol/szfdc/"
        # 定义将数据写入到test.txt文件
        self.file = open("test.txt", "w",encoding='utf-8')
    # 析构函数
    def __del__(self):
        self.file.close()
    #获取html txt
    def getHouseHtml(self,url):
        html = requests.get(url)
        text = html.text
        return text
    #解析房屋url数据
    def parseHouse(self,url):
        html = self.getHouseHtml(url)
        print(html)
        tree = etree.HTML(html, parser=etree.HTMLParser(encoding='utf-8'))
        nodes = tree.xpath('//div[@id="divShowList"]/tr')
        for node in nodes:
            # print node
            node1s = node.xpath('./td')
            for node1 in node1s:
                # print node1
                value = {}
                louceng = node1.xpath('./div/text()')
                detail = node1.xpath('./div/a/@href ')

                value["louceng"] = "".join(louceng)
                value["detail"] = ""
                if len(detail) != 0:
                    value["detail"] = "".join(detail)
                if len(value["detail"]) != 0:
                    value["detail"] = detailUrl + "".join(detail)
                    print(value["detail"])
                    text = self.getHouseHtml(value["detail"])
                    detail = value["louceng"] + ',' + self.getHouseDetail(text) + '\n'
                    self.file.write(detail.encode('utf-8').decode('utf-8'))
                    # print value["louceng"],value["detail"]

    def getHouseDetail(self,text):
        tree = etree.HTML(text, parser=etree.HTMLParser(encoding='utf-8'))
        nodes = tree.xpath('//tr')
        detail = ''
        for node in nodes:
            node1s = node.xpath('./td')
            value = {}
            for node1 in node1s:
                content = node1.xpath('./text()')
                tt = "".join(content)
                detail = detail + "," + tt
        detail = detail.replace(u'\r\n', '')
        detail = detail.replace(u'\a', '')
        return detail

bihai1 = 'http://ris.szpl.gov.cn/bol/building.aspx?id=32387&presellid=36452'
bihai2 = 'http://ris.szpl.gov.cn/bol/building.aspx?id=32387&presellid=36452&Branch=B&isBlock='
bihai3 = 'http://ris.szpl.gov.cn/bol/building.aspx?id=32386&presellid=36452'
bihai4 = 'http://ris.szpl.gov.cn/bol/building.aspx?id=32386&presellid=36452&Branch=B&isBlock='
bihai5 = 'http://ris.szpl.gov.cn/bol/building.aspx?id=32385&presellid=36452'
bihai6 = 'http://ris.szpl.gov.cn/bol/building.aspx?id=32385&presellid=36452&Branch=B&isBlock='
xiaoya = 'http://api.ximalaya.com/ximalayaos-picture-book/api/content/getAudio?albumId=06937&name=5&deviceId=18F0E416C676_9e6380f46382b857&appKey=70eefc246e3c4c749cb7c84d18859d4a&sn=11264_00_100264&sig=10163dd04c586096e5034a946c951f97'
shanhai1 = 'http://zjj.sz.gov.cn/ris/bol/szfdc/building.aspx?id=35383&presellid=42645'
shanhai2 = 'http://zjj.sz.gov.cn/ris/bol/szfdc/building.aspx?id=35384&presellid=42645'
shanhai3 = 'http://zjj.sz.gov.cn/ris/bol/szfdc/building.aspx?id=35385&presellid=42645'

if __name__ == '__main__':
    house = HouseToTxt()
    house.parseHouse(shanhai1)
    house.parseHouse(shanhai2)
    house.parseHouse(shanhai3)
