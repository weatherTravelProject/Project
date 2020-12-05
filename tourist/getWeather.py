"""
@File:getWeather
@Author:Sheng Yawen
@Date: 2020/11/13 
"""

import requests
import json
# 地区对应的id在weather_district_id.csv中
def get_district(location):
    # 城市的区名id
    guangzhou_list = [440100, 440103, 440104, 440105, 440106, 440111, 440112, 440113, 440114, 440115, 440117, 440118]
    shaoguan_list = [440200, 440203, 440204, 440205, 440222, 440224, 440229, 440232, 440233, 440281, 440282]
    shenzhen_list = [440300, 440303, 440304, 440305, 440306, 440307, 440308, 440309, 440310, 440311]
    zhuhai_list = [440400, 440402, 440403, 440404]
    shantou_list = [440500, 440507, 440511, 440512, 440513, 440514, 440515, 440523]
    foshan_list = [440600, 440604, 440605, 440606, 440607, 440608]
    jiangmen_list = [440700, 440703, 440704, 440705, 440781, 440783, 440784, 440785]
    zhanjiang_list = [440800, 440802, 440803, 440804, 440811, 440823, 440825, 440881, 440882, 440883]
    maoming_list = [440900, 440902, 440904, 440981, 440982, 440983]
    zhaoqing_list = [441200, 441202, 441203, 441204, 441223, 441224, 441225, 441226, 441284]
    huizhou_list = [441300, 441302, 441303, 441322, 441323, 441324]
    meizhou_list = [441400, 441402, 441403, 441422, 441423, 441424, 441426, 441427, 441481]
    shanwei_list = [441500, 441502, 441521, 441523, 441581]
    heyuan_list = [441600, 441602, 441621, 441622, 441623, 441624, 441625]
    yangjiang_list = [441700, 441702, 441704, 441721, 441781]
    qingyuan_list = [441800, 441802, 441803, 441821, 441823, 441825, 441826, 441881, 441882]
    chaozhou_list = [445100, 445102, 445103, 445122]
    jieyang_list = [445200, 445202, 445203, 445222, 445224, 445281]
    yunfu_list = [445300, 445302, 445303, 445321, 445322, 445381]

    list_id = {
        '广州': guangzhou_list,
        '佛山': foshan_list,
        '韶关': shaoguan_list,
        '深圳': shenzhen_list,
        '珠海': zhuhai_list,
        '汕头': shantou_list,
        '江门': jiangmen_list,
        '湛江': zhanjiang_list,
        '茂名': maoming_list,
        '肇庆': zhaoqing_list,
        '惠州': huizhou_list,
        '梅州': meizhou_list,
        '汕尾': shanwei_list,
        '河源': heyuan_list,
        '阳江': yangjiang_list,
        '清远': qingyuan_list,
        '东莞': [441900],
        '中山': [442000],
        '潮州': chaozhou_list,
        '揭阳': jieyang_list,
        '云浮': yunfu_list
    }
    # 返回对应城市的区名id
    try:
        return list_id[location]
    except KeyError as r:
        return False

def get_weather(district_list):
    # 判断是否为正确城市，否则退出
    if district_list == False:
        print("请输入正确城市！")
        return False
    api = "http://api.map.baidu.com/weather/v1/"

    for id in district_list:
        params = {
            'district_id': id,
            'ak': 'gAeroHY38EcqWGDplIBp1iTC1Mui5x8D',
            'data_type': 'all',
            'output': 'json'
        }

        r = requests.get(api, params=params)

        weather = r.text
        wea_list = eval(weather)

        location = wea_list['result']['location']['city'] + wea_list['result']['location']['name'] + '天气'

        fore_today = wea_list['result']['forecasts'][0]
        today_text = '今天天气：' + fore_today['text_day']
        today_weather = '气温：' + str(fore_today['low']) + '°至' + str(fore_today['high']) + '°'

        fore_tom = wea_list['result']['forecasts'][1]
        tom_text = '明天天气：' + fore_tom['text_day']
        tom_weather = '气温：' + str(fore_tom['low']) + '°至' + str(fore_tom['high']) + '°'

        print(location)
        print(today_text + "\t" + today_weather)
        print(tom_text + "\t" + tom_weather)

# 自主输入城市-待改进
get_weather(get_district('佛山'))