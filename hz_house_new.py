import importlib
import sys
importlib.reload(sys)
import requests
import lxml.etree as etree
import pandas as pd
import openpyxl
import os
import shutil


#detailUrl = 'http://ris.szpl.gov.cn/bol/'

detailUrl = 'http://data.fz0752.com/jygs/buildinglist.shtml'
class HouseToTxt():
    # 初始化函数
    def __init__(self):
        # 定义初始的文件路径，需要拼接
        self.detailUrl = "http://zjj.sz.gov.cn/ris/bol/szfdc/"
        self.listUrl = "http://data.fz0752.com/jygs/buildinglist.shtml"
        # 定义将数据写入到test.txt文件
        #self.file = open("test.txt", "w",encoding='utf-8')
    # 析构函数
    def __del__(self):
        #self.file.close()
        print(f'__del__:{self.detailUrl}')

    def opencsv(self):
        self.file = open(self.building_file, "a", encoding='utf-8')

    def closecsv(self):
        self.file.close()

    def copycsv(self,file,file_dir):
        shutil.copy(file, file_dir)

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
        #csv转换为excel，并去除掉无用列
        self.csv_to_excel()

    def csv_to_excel(self):
        csv_dir = "..\\szhouse\\"
        excel_dir = "..\\szhouse_excel\\"
        dataframe_dir = "..\\szhouse_excel_1\\"
        excel_suffix = f".xlsx"
        self.copycsv(self.building_file,csv_dir)
        name = self.building_file.split(".")[0]
        #csv转换为excel
        self.csv_to_excel_pd(f"{csv_dir}{self.building_file}",f"{excel_dir}{name}{excel_suffix}")
        #excel去掉无用列，并计算总价
        self.excel_to_dataFrame(f"{excel_dir}{name}{excel_suffix}",f"{dataframe_dir}{name}{excel_suffix}")

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
            node1s = node.xpath('.//div/a')
            for node1 in node1s:
                # print node1
                value = {}
                louceng = node1.xpath('./../preceding-sibling::div[1]/text()')
                detail = node1.xpath('./@href')
                value["louceng"] = "".join(louceng)
                value["detail"] = "".join(detail)
                if len(value["detail"]) != 0:
                    value["detail"] = detailUrl + value["detail"]
                    print(value["detail"])
                    text = self.getHouseHtml(value["detail"])
                    detail = value["louceng"]+self.getHouseDetail(text) + '\n'
                    self.file.write(detail.encode('utf-8').decode('utf-8'))

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

    #利用pandas将csv转换为excel文件
    def csv_to_excel_pd(self,src_file,dst_file):
            csv = pd.read_csv(src_file, encoding='utf-8')
            csv.to_excel(dst_file, sheet_name='data')

    #将csv目录的csv文件转换为excel文件
    def csv_to_excel_pd_dir(self):
        csv_dir = ''
        excel_dir = ''
        dataframe_dir = ''
        if (csv_dir == ''):
            csv_dir = "..\\szhouse\\"
        if (excel_dir == ''):
            excel_dir = "..\\szhouse_excel\\"
        if (dataframe_dir == ''):
            dataframe_dir = "..\\szhouse_excel_1\\"
        all_scv_file = []
        all_file = os.listdir(csv_dir)
        for filename in all_file:
            if ".csv" in filename:
                all_scv_file.append(filename)
        all_scv_file.sort()
        i = 0
        csv_file_num = len(all_scv_file)
        print(f"当前共有{csv_file_num}个csv文件需要转换，即将进行处理请稍等...")
        # 此层for循环是逐个csv文件进行处理
        for csv_file_name in all_scv_file:
            #self.csv_to_excel_pd(csv_file_name,)
            name = csv_file_name.split(".")[0]
            excel_suffix = f".xlsx"
            input_file_csv_path = f"{csv_dir}{csv_file_name}"
            out_file_excel_name = f"{excel_dir}{name}{excel_suffix}"
            dataframe_file_excel_name = f"{dataframe_dir}{name}{excel_suffix}"
            self.csv_to_excel_pd(input_file_csv_path,out_file_excel_name)
            self.excel_to_dataFrame(out_file_excel_name,dataframe_file_excel_name)

    def excel_to_dataFrame(self,src_file,dst_file):
        df = pd.DataFrame(pd.read_excel(src_file))
        #print(df)
        df.columns = list('abcdefghigklmnopqrstuvwxyz12')
        #取有用的列
        df1 = df.iloc[:,lambda df:[3,5,7,9,11,13,15,17,19,21]]
        df1.columns = [f"项目楼栋情况",f"座号",f"合同号",f"拟售价格(元/平方米)",f"楼层",f"房号",f"用途",f"建筑面积(平方米)",f"户内面积(平方米)",f"分摊面积(平方米)"]
        print(df1)
        #拟售价格去掉单位
        df1["拟售价格(元/平方米)"] = df1["拟售价格(元/平方米)"].str.replace("元/平方米","")
        df1["拟售价格(元/平方米)"] = df1["拟售价格(元/平方米)"].str.replace("按建筑面积计","")
        df1["拟售价格(元/平方米)"] = df1["拟售价格(元/平方米)"].str.replace("(","")
        df1["拟售价格(元/平方米)"] = df1["拟售价格(元/平方米)"].str.replace(")","")
        #已售出的价格替换成0
        df1["拟售价格(元/平方米)"] = df1["拟售价格(元/平方米)"].str.replace("--","0")
        #面积全部去掉单位
        df1["建筑面积(平方米)"] = df1["建筑面积(平方米)"].str.replace("平方米","")
        df1["户内面积(平方米)"] = df1["户内面积(平方米)"].str.replace("平方米","")
        df1["分摊面积(平方米)"] = df1["分摊面积(平方米)"].str.replace("平方米","")
        #计算总价
        df1["总价(元)"] = df1.apply(lambda x: round(float(x['拟售价格(元/平方米)']) * float(x['建筑面积(平方米)']),2), axis=1)
        df1["总价(万元)"] = df1.apply(lambda x: round(float(x['拟售价格(元/平方米)']) * float(x['建筑面积(平方米)'])/10000,2), axis=1)
        df1["总价*98折(万元)"] = df1.apply(lambda x: round(float(x['拟售价格(元/平方米)']) * float(x['建筑面积(平方米)'])*0.98/10000,2), axis=1)
        df1["使用率"] = df1.apply(lambda x:'{:.2%}'.format(float(x['户内面积(平方米)'])/float(x['建筑面积(平方米)'])),axis=1)
        print(df1)
        df1.to_excel(dst_file)
    def getBuildingList(self):

#此处从 http://data.fz0752.com/jygs/buildinglist.shtml 中查找到要爬取的楼盘地址。
channels = ["http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=43133",
            "http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=43093",
            "http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=43194",
            "http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=43233",
            "http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=43275",
            "http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=43373",
            "http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=43393"]
channels1 = ["http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=43713",
            "http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=43393",
            "http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=43373",
            "http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=43275",
            "http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=43233"]
channels2 = ["http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=43773",
             "http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=43793"]
channels3 = ["http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=38393"]

channels4 = ["http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=26087",
           "http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=39878"]

channels5 = ["http://zjj.sz.gov.cn/ris/bol/szfdc/projectdetail.aspx?id=43953"]

if __name__ == '__main__':
    for channel in channels5:
        house = HouseToTxt()
        house.parseBuilding(channel)
    #house.csv_to_excel_pd_dir()
    #house.parseBuilding(dehongtianxia)
    #house.parseBuilding(furunleting)
