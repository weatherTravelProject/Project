"""
@File:getWeather
@Author:Sheng Yawen
@Date: 2020/11/13 
"""

import requests

# 地区对应的id在weather_district_id.csv中
district_id = 130700

api = "http://api.map.baidu.com/weather/v1/"

# requ = "http://api.map.baidu.com/weather/v1/?district_id=130700&data_type=all&ak=gAeroHY38EcqWGDplIBp1iTC1Mui5x8D"

params = {
    'district_id': district_id,
    'ak': 'gAeroHY38EcqWGDplIBp1iTC1Mui5x8D',
    'data_type': 'all',
    'output': 'json'
}

r = requests.get(api, params=params)

print(r.json())