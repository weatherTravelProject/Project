"""
@File:tourist.py
@Author:Sheng Yawen
@Date: 2020/10/18 
"""
import time, requests, re  # time用于延时，requests用于请求网页数据，json转换json数据格式，re正则
import webbrowser
from lxml import etree  # 解析xpath网页结构
import pandas as pd  # 处理表格进行数据分析
import weather.final

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

def getPageNum(html):

    num = int(html.xpath('//*[@id="pager-container"]/div/a[last()-1]/text()')[0])
    return num

def getList(cityName):
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
    url = 'http://piao.qunar.com/ticket/list.htm?keyword=' + cityName + '&region=&from=mpl_search_suggest&sort=pp&page={}'
    # url = 'https://travel.qunar.com/p-cs300134-'+place+'-jingdian-1-{}'
    htm = requests.get(url, headers=headers)
    html = etree.HTML(htm.text)
    num = getPageNum(html)
    i = 1
    sightlist = []
    while i < 3:
        page = getPage(url.format(i))  # 这里调用了getPage函数获取了网页数据
        selector = etree.HTML(page.text)
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
            sight_add = inf.xpath('.//p[@class ="address color999"]/span/text()')[0]
            sight_add = re.sub('地址：|（.*?）|\(.*?\)|，.*?$|\/.*?$', '', str(sight_add))
            sight_slogen = inf.xpath(".//div[@class='intro color999']/text()")
            if len(sight_slogen):
                sight_slogen = sight_slogen[0]
            else:
                sight_slogen = ' '
            sight_point = inf.xpath('.//@data-point')[0]
            print(sight_point)
            # .为当前序号，不加则从第一个开始
            sightlist.append([cityName, sight_name, sight_level, sight_add.replace('地址：', ''), sight_point, sight_slogen])
        time.sleep(2)
    return sightlist


def listToExcel(list, name):
    # df = pd.DataFrame(list, columns=['景点名称', '级别', '所在区域', '起步价', '销售量', '热度', '地址', '经纬度', '标语', '详情网址'])
    df = pd.DataFrame(list)
    dirName = 'data/'
    df.to_csv( dirName + name + ".csv", sep=',', header=None)
    # writer = pd.ExcelWriter(dirName+'/hotplace.xlsx', engine='xlsxwriter')
    # df.to_excel(writer, sheet_name='Sheet1')
    # writer.save()


def main():
    while(weather.final.cityname):
        sightlist = getList(weather.final.cityname)  # main后第一个运行getList()
        listToExcel(sightlist, 'hotplace')
        break
    webbrowser.open("http://localhost:63342/Project/weather/data/gdMap.html")

if __name__ == '__main__':  # 代码是从main函数开始的
    main()