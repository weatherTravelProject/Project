"""
@File:tourist.py
@Author:Sheng Yawen，Yuying
@Date: 2020/10/18
"""

import time, requests, re  # time用于延时，requests用于请求网页数据，json转换json数据格式，re正则
from lxml import etree  # 解析xpath网页结构
import pandas as pd  # 处理表格进行数据分析
import math

def getPage(url):  # 获取链接中的网页内容
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'cookie': 'QN1=O5cv7V3FXX6RVSo2FsZGAg==; QN205=s%3Dgoogle; QN277=s%3Dgoogle; csrfToken=AUBSZ1SJgtl2cBX2HyuS2BTEXvmciXKc; _i=RBTKS082R8KxQVZx6JB9OtPmNyxx; QN269=1EDA0650022211EA926DFA163E72396C; fid=3ac01f31-9181-4ed7-a38a-5c0d137aefcc; QN99=1500; QN300=organic; QunarGlobal=10.86.213.148_-72515c99_16e4b45ba14_623b|1573223249997; _vi=hCXRv3fD46caoElZPDCXIreqcskT0Spj7f9XqyWhjfxmL_u3Y7xhSmU49JoeKnflmT0XtDD78wrAbOYIR_IG3FwU-fkUzn927J70W0JK0Iy219BfJnqA_WGLcMw_p8UHFhEtG9kQ-SOa3-aG4lJkhxTME8JhUdpjG4Kl7_X1KFGy; QN601=28e00ebdfc5eae6e44c48a34869c6dd1; QN163=0; QN667=B; QN48=09fd9580-c998-4f2a-bd31-516ddfaeb4f3; QN100=WyLlpKfov57mma%2Fngrl85aSn6L%2BeIl0%3D; QN243=19; JSESSIONID=568D43DF4624B99A32042DCC50F984B8; QN57=15732237429980.552477010226762; Hm_lvt_15577700f8ecddb1a927813c81166ade=1573223744; QN267=91363111d04a42d3; QN58=1573223742995%7C1573223864461%7C2; Hm_lpvt_15577700f8ecddb1a927813c81166ade=1573223865; QN271=88a69a10-00a3-42e0-a9dd-dcd01d16ca04',
        'Host': 'piao.qunar.com',
        'Referer': 'http://piao.qunar.com/ticket/list.htm?keyword=%E7%83%AD%E9%97%'
                   'A8%E6%99%AF%E7%82%B9&region=&from=mpl_search_suggest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    try:
        page = requests.get(url, headers=headers)  # 这里是请求网页数据了
        return page
    except Exception as e:
        print(str(e))

def getPageNum(content):
    num = int(content.xpath('//*[@id="pager-container"]/div/a[last()-1]/text()')[0])
    while num:
        search_number = input("请输入需要查询数据数目：（请输入10的整数倍数目）")
        while search_number:
            if int(search_number) % 10 == 0 and int(search_number) // 10 <= num:
                print("输入数目正确")
                print("您的输入是：" + search_number)
                break
            else:
                print("您的输入有误")
                search_number = input("请输入需要查询数据数目：（请输入10的整数倍数目）")
        break
    true_number = int(math.ceil(int(search_number) / 10))  # 小数向上取整ceil
    print("实际查询页数为：", true_number)
    return true_number
    #num = int(html.xpath('//*[@id="pager-container"]/div/a[last()-1]/text()')[0])
    #return num



def gethtml(url):
    header = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
    #url = 'http://piao.qunar.com/ticket/list.htm?keyword=%E5%B9%BF%E4%B8%9C&region=&from=mpl_search_suggest&city=' + place + '&page={}&subject=&sort=pp'
    htm = requests.get(url, header, timeout=30)
    html = etree.HTML(htm.text)
    return html


def getList(content,num,url):
    i = 1
    sightlist = []
    while i <= num:
        selector  = gethtml(url.format(i))  # 这里调用了getPage函数获取了网页数据
        #selector = etree.HTML(page)
        print('正在爬取第', str(i), '页景点信息')
        i += 1
        # 下面生成的是列表
        informations = selector.xpath('.//div[@class="result_list"]/div')
        for inf in informations:  # 获取必要信息
            sight_name = inf.xpath('.//a[@class="name"]/@title')[0]
            print(sight_name)
            sight_level = inf.xpath('.//span[@class="level"]/text()')
            if len(sight_level):
                sight_level = sight_level[0].replace('景区', '')
            else:
                sight_level = 0
            # sight_area = inf.xpath('.//span[@class="area"]/a/text()')[0]
            sight_add = inf.xpath('.//p[@class ="address color999"]/span/text()')[0]
            sight_add = re.sub('地址：|（.*?）|\(.*?\)|，.*?$|\/.*?$', '', str(sight_add))
            sight_slogen = inf.xpath(".//div[@class='intro color999']/text()")
            if len(sight_slogen):
                sight_slogen = sight_slogen[0]
            else:
                sight_slogen = ' '
            # sight_price = inf.xpath(".//span[@class='sight_item_price']/em/text()")
            # if len(sight_price):
            #     sight_price = sight_price[0]
            # else:
            #     sight_price = 0
            # sight_soldnum = inf.xpath('.//span[@class="hot_num"]/text()')
            # if len(sight_soldnum):
            #     sight_soldnum = sight_soldnum[0]
            # else:
            #     sight_soldnum = 0
            # sight_point = inf.xpath('.//div[@class="result_list"]/div/@data-point')[0]
            sight_point = inf.xpath('.//@data-point')[0]
            # sight_la, sight_lo = sight_point.split(',')
            print(sight_point)
            # .为当前序号，不加则从第一个开始
            sight_url = inf.xpath('.//div[@class="sight_item_pop"]//a/@href')[0]
            sightlist.append([sight_name, sight_level,sight_add.replace('地址：', ''), sight_point, sight_slogen, sight_url])
        time.sleep(2)
    return sightlist


def listToExcel(list, name):
    # df = pd.DataFrame(list, columns=['景点名称', '级别', '所在区域', '起步价', '销售量', '热度', '地址', '经纬度', '标语', '详情网址'])
    df = pd.DataFrame(list)
    dirName = 'html/'
    df.to_csv( dirName + name + ".csv", sep=',', header=None)
    # writer = pd.ExcelWriter(dirName+'/hotplace.xlsx', engine='xlsxwriter')
    # df.to_excel(writer, sheet_name='Sheet1')
    # writer.save()


def main():
    '''url = "https://travel.qunar.com/place/"
    html = general_unit.get_content(url)
    get_traval_list(html)
    general_unit.data_save(travel_list, 'travel_list.csv')
    city = input("城市")
    while city:
        if not dic_for_search.get(city) is None:
            print("您的输入是：" + city)
            url = dic_for_search.get(city)
            break
        else:
            print("您的输入有误")'''
    num=0
    citys=['广州','深圳','珠海','东莞','清远','佛山','惠州','中山','肇庆','河源','江门','汕头','湛江','潮州','阳江','梅州','茂名','汕尾']
    place=input("请输入需要城市(目前仅支持广东地区)：")
    while place:
        if place not in set(citys):
            print("未查阅到该城市景点信息")
            place = input("请输入其他需要城市：")
        else:
            print("您的输入是：" + place)
            url='http://piao.qunar.com/ticket/list.htm?keyword=%E5%B9%BF%E4%B8%9C&region=&from=mpl_search_suggest&city=' + place + '&page={}&subject=&sort=pp'
            break
    content=gethtml(url)
    num=getPageNum(content)
    sightlist = getList(content,num,url)  # main后第一个运行getList()
    listToExcel(sightlist, 'hotplace')


if __name__ == '__main__':  # 代码是从main函数开始的
    main()