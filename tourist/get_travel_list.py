"""
@File:get_travel_list.py
@Author:Yuying
@Date:2020/10/25
"""
import traceback
from bs4 import BeautifulSoup
from tourist import general_unit

#全局变量定义
diqus=[]
diqus2=[]
travel_list=[]

def get_traval_list(html):
    n=0  #定义一个n获取得到的信息数目
    soup=BeautifulSoup(html,"html.parser")
    first=soup.find('div',class_='list current')
    diqus=first.find_all('div',class_='sub_list')
    for diqu in diqus:
        diqus2=diqu.find_all('a',class_='link')
        for diqu2 in diqus2:                #待优化项：优化查询时间，减少时间复杂度
            try:
                dic_for_save={}  #定义一个字典，用于保存后输出
                dic_for_search={} #定义一个字典，用于搜索
                city_name=diqu2.string  #循环获取城市名称
                n+=1
                href1=diqu2.attrs['href'] #循环获取城市链接
                href=href1+'-jingdian'
                dic_for_save.update({'城市名称':city_name,'景点对应链接':href})
                dic_for_search.update({city_name:href})
                travel_list.append(dic_for_save)   #由于暂时没找到更好的保存方式，此处用了两个字典进行存储
                print("{}.成功爬取{}对应景点链接信息".format(n,city_name))
            except Exception as e:
                print("错误类型为：", e.__class__.__name__)
                print("错误详情为：", e)
                traceback.print_exc()

if __name__=="__main__":
   url="https://travel.qunar.com/place/"
   html= general_unit.get_content(url)
   get_traval_list(html)
   general_unit.data_save(travel_list, 'travel_list.csv')
