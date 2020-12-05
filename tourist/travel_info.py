"""
@File:get_travel_list.py
@Author:Yuying
@Date:2020/11/01
"""
from bs4 import BeautifulSoup
from tourist import general_unit
import math
import traceback

#全局变量定义
url_list=[]#定义一个url的列表
travel_info=[]
diqus=[]
diqus2=[]
travel_list=[]
dic_for_search={}
dic_for_save={}

def get_url(url,page_number):
    for number in range(1,page_number+1):
        search_url=url+"-1-%s"%number
        url_list.append(search_url)#将不同页数的网址添加到urllist中
    return url_list

def get_travel_info(html):
    n=0
    dic={}
    soup=BeautifulSoup(html,"html.parser")
    ul = soup.find('ul', class_='list_item clrfix')
    lis = ul.find_all('li')
    for li in lis:
        data_lat=li['data-lat']# 景点的位置
        data_lng=li['data-lng']# 景点的位置
        #Chinese_name
        #English_name   #待信息优化：拆分英文名和中文名
        name=li.select('.cn_tit ')[0].text# 景点名称
        num=li.select('.comment_sum')[0].text# 景点点评数
        star=li.select('.cur_star')[0]['style'].split(":")[1]# 景点评分
        cishu=li.select('.strategy_sum')[0].text# 景点攻略提到的次数

        #存储数据入字典中
        n+= 1
        dic['data_lat']=data_lat
        dic['data_lng'] = data_lng
        dic['name'] = name
        dic['num'] = num
        dic['star'] = star
        dic['cishu'] = cishu

        temp = str(dic)   #解决插入字典变量到数组中的问题
        temp2 = eval(temp)
        travel_info.append(temp2)
        print('成功采集第%s条数据'% n)
    return travel_info


def control_page():#n是输入需要获取的信息数
    search_number = input("请输入需要查询数据数目：（请输入10的整数倍数目）")
    while search_number:
        if int(search_number) % 10 == 0:
            print("输入数目正确")
            print("您的输入是：" + search_number)
            break
        else:
            print("您的输入有误")
            search_number = input("请输入需要查询数据数目：（请输入10的整数倍数目）")
    true_number = int(math.ceil(int(search_number) / 10))  # 小数向上取整ceil
    print("实际查询页数为：", true_number)
    return true_number

def get_traval_list(html):
    n=0  #定义一个n获取得到的信息数目
    soup=BeautifulSoup(html,"html.parser")
    first=soup.find('div',class_='list current')
    diqus=first.find_all('div',class_='sub_list')
    for diqu in diqus:
        diqus2=diqu.find_all('a',class_='link')
        for diqu2 in diqus2:                #待优化项：优化查询时间，减少时间复杂度
            try:
                city_name=diqu2.string  #循环获取城市名称
                n+=1
                href1=diqu2.attrs['href'] #循环获取城市链接
                href=href1+'-jingdian'
                dic_for_save.update({'城市名称':city_name,'景点对应链接':href})
                dic_for_search.update({city_name:href})
                temp = str(dic_for_save)  # 解决插入字典变量到数组中的问题
                temp2 = eval(temp)
                travel_list.append(temp2) #由于暂时没找到更好的保存方式，此处用了两个字典进行存储
                print("{}.成功爬取{}对应景点链接信息".format(n,city_name))
                #return dic_for_save
            except Exception as e:
                print("错误类型为：", e.__class__.__name__)
                print("错误详情为：", e)
                traceback.print_exc()



if __name__=="__main__":
    url = "https://travel.qunar.com/place/"
    html = general_unit.get_content(url)
    get_traval_list(html)
    general_unit.data_save(travel_list, 'travel_list.csv')
    print(dic_for_search)
    city = input("请输入需要城市：")
    while city:
        if not dic_for_search.get(city) is None:
            print("您的输入是：" + city)
            url=dic_for_search.get(city)
            break
        else:
            print("您的输入有误")
    page_number = control_page()
    #url='https://travel.qunar.com/p-cs299878-shanghai-jingdian'
    get_url(url,page_number)
    for l in url_list:  ##遍历url_list的url
        print(l)
        info= general_unit.get_content(l)
        get_travel_info(info)
    general_unit.data_save(travel_info, 'travel_info.csv')
