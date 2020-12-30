import requests
import urllib.request
from urllib.parse import quote
from bs4 import BeautifulSoup  # 解析页面模块
import re    
#re模块是python独有的匹配字符串的模块，该模块中提供的很多功能是基于正则表达式实现的
from pyecharts import Geo
#from pyecharts.charts import Geo, Map
import os
 
import csv
import pygal
import cityinfo

def get_weather():
    root_path = os.path.abspath(os.path.dirname(__file__))
    save_path = root_path+'/data/'
    print(save_path)
    ''' 广东省21个行政区 '''
    name0 = ['广州','深圳','珠海','汕头','佛山','韶关','湛江','肇庆','江门','茂名','惠州','梅州','汕尾','河源','阳江','清远','东莞','中山','潮州','揭阳','云浮']

    headers={'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    lowTemp = []  # 记录最低气温
    highTemp = [] # 记录最高气温

    for i in range(len(name0)):
        name = quote(name0[i]) # URL编码，quote的作用是把name0里的字符转换为%xx格式

        '''获取城市代号编码'''
        url0 = 'http://toy1.weather.com.cn/search?cityname={}'.format(name)
        html0 = urllib.request.urlopen(url0)
        html0 = html0.read().decode('utf-8')
        code = re.search(r'\d{9}' , html0).group()  #匹配html0里面的第一串9位数（每个城市的编码，用于下面url的编写）；\d是元字符，r'\d'与'\\d'相同，在字符串之前加r，让整个字符串不转义

        url = "http://www.weather.com.cn/weather/{}.shtml".format(code)

        res = requests.get(url,headers=headers)
        res.encoding='utf-8'
        bs=BeautifulSoup(res.text,'html.parser')

        tem1= bs.find(class_='tem')
        weather1= bs.find(class_='wea')
        wind1 = bs.find(class_='win')
        tem=tem1.text
        weather=weather1.text
        wind=wind1.find('span')['title']+' '+wind1.text.strip()
        print(name0[i]+':')
        print(tem+weather)
        print(wind)

        if tem1.find('span') is None:
            temperature_highest = None # 天气预报可能没有当天的最高气温（到了傍晚会出现这种情况）
        else:
            temperature_highest = tem1.find('span').string # 找到最高温度
            temperature_highest = temperature_highest.replace('℃', '') # 到了晚上网站会变，最高温度后面也有个℃
        temperature_lowest = tem1.find('i').string  # 找到最低温度
        temperature_lowest = temperature_lowest.replace('℃', '')  # 最低温度后面有个℃，去掉这个符号

        highTemp.append(temperature_highest)
        lowTemp.append(temperature_lowest)

        print('\r成功获取{}的气温情况...'.format(name0[i]))
        print('-------------------------------')


    geo = Geo("广东省行政区最低气温", "Low Temperature",  page_title='广东省行政区最低气温图',
        title_color="#fff", title_pos="center",width=1200, height=600,
        background_color='#404a59')   #绘画地图
    attr, value = name0, lowTemp
    geo.add("", attr, value, visual_range=[-10, 30], maptype='广东',label_formatter='{b}',
        visual_text_color="#fff", symbol_size=13, is_visualmap=True,is_label_show = True,
        label_text_color="#00FF00", type="effectScatter",effect_scale=3)
    geo.render(save_path + '广东省行政区最低气温图.html')
    print('广东省行政区最低气温图生成成功！')

    geo = Geo("广东省行政区最高气温", "High Temperature",  page_title='广东省行政区最高气温图',
        title_color="#fff", title_pos="center",width=1200, height=600,
        background_color='#404a59')   #绘画地图
    attr, value = name0, highTemp
    geo.add("", attr, value, visual_range=[-10, 30], maptype='广东',label_formatter='{b}',
        visual_text_color="#fff", symbol_size=13, is_visualmap=True,is_label_show = True,
        label_text_color="#00FF00", type="effectScatter",effect_scale=3)
    geo.render(save_path + '广东省行政区最高气温图.html')
    print('广东省行政区最高气温图生成成功！')

    while True:
        cityname = input("\n请输入你想要查询天气的城市:")
        if cityname in cityinfo.city:
            citycode = cityinfo.city[cityname]
            break
        else:
            print('没有此城市哦，请输入正确的城市名称')
    url1 = 'http://www.weather.com.cn/weather/' + citycode + '.shtml'
    res1 = requests.get(url1,headers=headers)
    res1.encoding='utf-8'

    # 根据得到的页面信息进行初步筛选过滤
    final = []  # 初始化一个列表保存数据
    bs = BeautifulSoup(res1.text, "html.parser")  # 创建BeautifulSoup对象
    body = bs.body
    data = body.find('div', {'id': '7d'})
    # print(type(city_data))
    ul = data.find('ul')
    li = ul.find_all('li')

    # 爬取自己需要的数据
    i = 0  # 控制爬取的天数
    lows = []  # 保存低温
    highs = []  # 保存高温
    daytimes = []  # 保存日期
    weathers = []  # 保存天气
    for day in li:  # 便利找到的每一个li
        if i < 7:
            temp = []  # 临时存放每天的数据
            date = day.find('h1').string  # 得到日期
            #print(date)
            temp.append(date)
            daytimes.append(date)
            inf = day.find_all('p')  # 遍历li下面的p标签 有多个p需要使用find_all 而不是find

            #print(inf[0].string)  # 提取第一个p标签的值，即天气
            temp.append(inf[0].string)
            weathers.append(inf[0].string)
            temlow = inf[1].find('i').string  # 最低气温
            if inf[1].find('span') is None:  # 天气预报可能没有最高气温
                temhigh = None
                temperate = temlow
            else:
                temhigh = inf[1].find('span').string  # 最高气温
                temhigh = temhigh.replace('℃', '')
                temperate = temhigh + '/' + temlow
            # temp.append(temhigh)
            # temp.append(temlow)
            lowStr = ""
            lowStr = lowStr.join(temlow.string)
            lows.append(int(lowStr[:-1]))  # 以上三行将低温NavigableString转成int类型并存入低温列表
            if temhigh is None:
                highs.append(int(lowStr[:-1]))
            else:
                highStr = ""
                highStr = highStr.join(temhigh)
                highs.append(int(highStr))  # 以上三行将高温NavigableString转成int类型并存入高温列表
            temp.append(temperate)
            final.append(temp)
            i = i + 1

    # 将最终的获取的天气写入csv文件
    with open(save_path + 'weather.csv', 'w', errors='ignore', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows([cityname])
        f_csv.writerows(final)
    print('\ncsv文件编写成功')

    # 绘图
    bar = pygal.Line()  # 创建折线图
    bar.add('最低气温', lows)  #添加两线的数据序列
    bar.add('最高气温', highs)  #lows和highs是int型的列表

    bar.x_labels = daytimes  #  x轴坐标数据
    bar.x_label_rotation = 45  #倾斜45度

    bar.title = cityname+'未来七天气温走向图'    #设置图形标题
    bar.x_title = '日期'   #   x轴标题
    bar.y_title = '气温(摄氏度)'  #  y轴标题

    bar.legend_at_bottom = True
    bar.show_x_guides = False
    bar.show_y_guides = True

    bar.render_to_file(save_path + 'temperate.svg')
    print('\ncsv文件保存成功,可以使用浏览器打开哦')
    return cityname

if __name__=="__main__":
    cityname=get_weather()
    print(cityname)


