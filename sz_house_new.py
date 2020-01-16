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
        #self.file = open("test.txt", "w",encoding='utf-8')
    # 析构函数
    def __del__(self):
        #self.file.close()
        print(f'__del__:{self.detailUrl}')

    def opencsv(self):
        self.file = open(self.building_file, "w", encoding='utf-8')

    def closecsv(self):
        self.file.close()

    #根据项目url获取所有楼栋以及branch数据
    def  parseBuilding(self,url):
        #获取项目名称，设置生成文件名为项目名称
        self.getBuildingName(url)
        #打开文件
        self.opencsv()
        buildings = self.getBuilding(url)
        for building in buildings:
            branchs = self.getBranch(building)
            for branch in branchs:
                self.parseHouse(branch)
        #关闭文件
        self.closecsv()


    def getBuildingName(self,url):
        html = self.getHouseHtml(url)
        print(html)
        tree = etree.HTML(html, parser=etree.HTMLParser(encoding='utf-8'))
        name = tree.xpath('.//table[@class="table ta-c table2 table-white"][1]/tr[1]/td[2]/text()')
        building_name = "".join(name).replace(u'\r\n','').strip()
        self.building_file = f'{building_name}.csv'

    #根据url 获取楼栋url
    def getBuilding(self,url):
        html = self.getHouseHtml(url)
        print(html)
        tree = etree.HTML(html, parser=etree.HTMLParser(encoding='utf-8'))
        building =[]
        nodes = tree.xpath('.//table[@class="table ta-c table2 table-white"]/tr/td/a/@href')
        for node in nodes:
            if len(node) != 0:
                building.append(self.detailUrl+node)
        return building

    #获取每栋的座号url
    def getBranch(self,url):
        html = self.getHouseHtml(url)
        print(html)
        tree = etree.HTML(html, parser=etree.HTMLParser(encoding='utf-8'))
        branchs =[]
        nodes = tree.xpath('.//div[@id="divShowBranch"]')
        for node in nodes:
            node1s = node.xpath('./a/@href')
            if len(node1s) != 0:
                for branch in node1s:
                 branchs.append(self.detailUrl+branch)
        return branchs


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
            #node1s = node.xpath('./td')
            node1s = node.xpath('.//div/a')
            for node1 in node1s:
                # print node1
                value = {}
                louceng = node1.xpath('./../preceding-sibling::div[1]/text()')
                #detail = node1.xpath('./div/a/@href')
                detail = node1.xpath('./@href')
                value["louceng"] = "".join(louceng)
                value["detail"] = "".join(detail)
                #if len(detail) != 0:
                    #value["detail"] = "".join(detail)
                if len(value["detail"]) != 0:
                    value["detail"] = detailUrl + value["detail"]
                    print(value["detail"])
                    text = self.getHouseHtml(value["detail"])
                    detail = value["louceng"]+self.getHouseDetail(text) + '\n'
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
                tt = tt.replace(u'\r\n', '').strip()
                detail = detail + "," + tt
        detail = detail.replace(u'\r\n', '')
        detail = detail.replace(u'\a', '')
        return detail

#此处从http://zjj.sz.gov.cn/ris/bol/szfdc/index.aspx 中查找到要爬取的楼盘地址。
bihai1 = 'http://ris.szpl.gov.cn/bol/building.aspx?id=32387&presellid=36452'
bihai2 = 'http://ris.szpl.gov.cn/bol/building.aspx?id=32387&presellid=36452&Branch=B&isBlock='
bihai3 = 'http://ris.szpl.gov.cn/bol/building.aspx?id=32386&presellid=36452'
bihai4 = 'http://ris.szpl.gov.cn/bol/building.aspx?id=32386&presellid=36452&Branch=B&isBlock='
bihai5 = 'http://ris.szpl.gov.cn/bol/building.aspx?id=32385&presellid=36452'
bihai6 = 'http://ris.szpl.gov.cn/bol/building.aspx?id=32385&presellid=36452&Branch=B&isBlock='
shanhai1 = 'http://zjj.sz.gov.cn/ris/bol/szfdc/building.aspx?id=35383&presellid=42645'
shanhai2 = 'http://zjj.sz.gov.cn/ris/bol/szfdc/building.aspx?id=35384&presellid=42645'
shanhai3 = 'http://zjj.sz.gov.cn/ris/bol/szfdc/building.aspx?id=35385&presellid=42645'
huarun1 = 'http://zjj.sz.gov.cn/ris/bol/szfdc/building.aspx?id=35508&presellid=42854'
huarun2 = 'http://zjj.sz.gov.cn/ris/bol/szfdc/building.aspx?id=35509&presellid=42854'
huarun = 'http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=42854'
luhui = 'http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=42584'
shanhai = 'http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=42645'
lvdi ='http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=42833'
huizhi='http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=42829'
chunjiang='http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=42824'
qinchengda='http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=42823'
longguang='http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=42816'
qianhai='http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=42808'
huizhan='http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=42741'
baochang ='http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=42713'
baochang2='http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=42699'
jiazhaoye='http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=42593'
dehong='http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=42953'
furun='http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=42934'
shenshan='http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=42884'
kaiyuna='http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=42881'
zhidi='http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=42854'
zhongdian='http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=42640'
jingji='http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=42583'
zhenye='http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=42579'
huihuang='http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=42641'
shenwan='http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=42683'
zhonghai='http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=42716'
jiulongtai='http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=42725'
beiyuehui='http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=42993'
dehongtianxia='http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=42953'
furunleting='http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=42934'
if __name__ == '__main__':
    house = HouseToTxt()
    house.parseBuilding(beiyuehui)
    house.parseBuilding(dehongtianxia)
    house.parseBuilding(furunleting)
