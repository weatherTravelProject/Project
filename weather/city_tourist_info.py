"""
@File:tourist.py
@Author:Sheng Yawen，Yuying
@Date: 2020/10/18
"""

import time, requests, re  # time用于延时，requests用于请求网页数据，json转换json数据格式，re正则
from lxml import etree  # 解析xpath网页结构
import pandas as pd  # 处理表格进行数据分析
import math
import get_weather
import webbrowser
from bs4 import BeautifulSoup


def getPageNum(content):
    num = int(content.xpath('//*[@id="pager-container"]/div/a[last()-1]/text()')[0])
    while num:#此处循环进行输入校验
        search_number = input("请输入需要查询数据数目：（请输入10的整数倍数目）")
        while search_number:#将输入的数据数目转换为需要的页码数
            if int(search_number) % 10 == 0 and int(search_number) / 10 <= num:
                print("输入数目正确")
                print("您的输入是：" + search_number)#输入正确,获得需要搜索的页码值
                break
            else:
                print("您的输入有误")
                search_number = input("请输入需要查询数据数目：（请输入10的整数倍数目）")#输入错误进入循环,再次输入
        break
    true_number = int(math.ceil(int(search_number) / 10))  # 小数向上取整ceil
    print("实际查询页数为：", true_number)
    return true_number
    #num = int(html.xpath('//*[@id="pager-container"]/div/a[last()-1]/text()')[0])
    #return num

#获取网页某一页的信息
def gethtml(url):
    header = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
    #url = 'http://piao.qunar.com/ticket/list.htm?keyword=%E5%B9%BF%E4%B8%9C&region=&from=mpl_search_suggest&city=' + place + '&page={}&subject=&sort=pp'
    htm = requests.get(url, header, timeout=30)
    html = etree.HTML(htm.text)
    return html


def getList(num,url):
    i = 1
    sightlist= []
    echartlist=[]
    while i <= num:
        selector = gethtml(url.format(i))  # 这里调用了getPage函数获取了网页数据
        # selector = etree.HTML(page)
        print('正在爬取第', str(i), '页景点信息')
        i += 1
        # 下面生成的是列表
        informations = selector.xpath('.//div[@class="result_list"]/div')
        for inf in informations:  # 获取必要信息
            sight_name = inf.xpath('.//a[@class="name"]/@title')[0] # 爬取景点名
            print(sight_name)
            sight_level = inf.xpath('.//span[@class="level"]/text()') # 爬取景点级别
            if len(sight_level):
                sight_level = sight_level[0].replace('景区', '')
            else:
                sight_level = 0
            sight_hot = inf.xpath('.//span[@class="product_star_level"]//span/text()')[0].replace('热度 ', '') # 景点热度
            sight_add = inf.xpath('.//p[@class ="address color999"]/span/text()')[0]
            sight_add = re.sub('地址：|（.*?）|\(.*?\)|，.*?$|\/.*?$', '', str(sight_add)) # 景点地址
            sight_slogen = inf.xpath(".//div[@class='intro color999']/text()") # 景点介绍
            # 若无景点介绍则设为空格
            if len(sight_slogen):
                sight_slogen = sight_slogen[0]
            else:
                sight_slogen = ' '
            sight_point = inf.xpath('.//@data-point')[0]
            print(sight_point)
            # .为当前序号，不加则从第一个开始
            sight_url = inf.xpath('.//div[@class="sight_item_pop"]//a/@href')[0]
            sightlist.append([sight_name, sight_level,sight_add.replace('地址：', ''), sight_point, sight_slogen, sight_url])
            echartlist.append([sight_name,sight_hot]) #保存到echartlist的列表中,方便之后单独存储为一个文件,便于后续可视化分析
        time.sleep(0.5)
    return sightlist,echartlist

def listToExcel(list, name):
    df = pd.DataFrame(list)
    dirName = 'data/'
    df.to_csv(dirName + name + ".csv", sep=',', header=None,index=False)

def get_tourist_info_byNum(cityname):
    url='http://piao.qunar.com/ticket/list.htm?keyword=%E5%B9%BF%E4%B8%9C&region=&from=mpl_search_suggest&city=' + cityname + '&page={}&subject=&sort=pp'
    content=gethtml(url.format(1))#通过爬取第一页,获取总页数,此处是爬取第一页
    num=getPageNum(content)#通过爬取第一页,获取总页数,此处是获取总页数
    sightlist, echartlist = getList(num,url)  # 通过获取需要的信息数量,返回指定页面信息
    listToExcel(sightlist, 'hotplace')
    listToExcel(echartlist,'csv_toEchart')
    webbrowser.open("http://localhost:63342/Project/weather/data/gdMap.html")


def main():
    get_tourist_info_byNum("佛山")

if __name__ == '__main__':  # 代码是从main函数开始的
    main()