# 导包
import get_weather
import city_tourist_info
import city_to_echart

# 主函数
def main():
    cityname = get_weather.get_weather()   # 爬取天气，获取输入的城市名
    print("需要获取旅游信息的城市为：" + cityname) # 打印城市名
    city_tourist_info.get_tourist_info_byNum(cityname) # 爬取城市景点
    # 生成景区图和柱状图
    city_to_echart.top_10_echart()
    city_to_echart.SceneryGrade_ecahrt()

if __name__ == '__main__':
    main()