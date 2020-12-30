from pyecharts import Bar,Pie
#from pyecharts import options as opts
import pandas as pd
import numpy as np

# 需要注意使用的是5.0.11的pyechart,绘制的都是所选城市相关信息图
# 使用的时候需要安装主题插件pip install echarts-themes-pypkg

# 排名前十景点热度-柱状图
def top_10_echart():
    hot_list = []
    name_list = []
    # 数据读取及解析
    ##  读取csv文件数据
    data = pd.read_csv('data/csv_toEchart.csv',header=None)
    array_data = np.array(data)  # 先将数据框转换为数组
    list_data = array_data.tolist()  # 其次转换为列表
    print(data)
    ##  解析x轴数据
    for name in list_data[0:10]:
        name_list.append(str(name[0]))
    ##  解析y轴数据
    for hot in list_data[0:10]:
        hot_list.append(str(float(hot[1])))
    #print(hot_list)

    #绘图设置
    bar=Bar(title="排名前十景点热度-柱状图",subtitle="热度为0景点的不进行统计",height=500,width=1200)
    bar.use_theme('vintage')# 选择了VINTAGE主题进行展示
    #设置主标题为景点热度,x轴数据时name_list,y轴数据是hot_list,,将最高点和最低点标记出来,使用标记线记录平均值
    bar.add("景点热度",name_list,hot_list,markpoint=["max", "min"],mark_line=["average"],xaxis_interval=0, xaxis_rotate=20, yaxis_rotate=20)
    bar.render('data/排名前十景点热度-柱状图.html') # 生成本地文件（默认为.html文件）
    print("\n排名前十景点热度-柱状图.html文件生成成功,可以使用浏览器打开哦")

#5a,4a景区占比及数量-饼图
def SceneryGrade_ecahrt():
    SceneryGrade=[]
    num_5a=num_4a=num_3a=num_other=0
    # 数据读取及解析
    ##  读取csv文件数据
    data = pd.read_csv('data/hotplace.csv',header=None)
    array_data = np.array(data)  # 先将数据框转换为数组
    list_data = array_data.tolist()  # 其次转换为列表
    ##  解析景区级别
    for grade in list_data:
        if str(grade[1])=='4A':
            num_4a+=1  #当前城市拥有5a景区数目
        if str(grade[1])=='5A':
            num_5a+=1
        if str(grade[1])=='3A':
            num_3a+=1
        else:
            num_other+=1
        SceneryGrade.append(str(grade[1]))
    grade=["当前城市拥有5a景区数目","当前城市拥有4a景区数目","其他景区"]
    num=[num_5a,num_4a,num_other]

    #绘图设置
    pie=Pie(title="5a,4a景区占比及数量-饼图", subtitle="按照中华人民共和国旅游景区质量等级划分")
    pie.use_theme('vintage')  # 选择了VINTAGE主题进行展示
    pie.add("景区占比",grade,num,is_label_show=True)
    pie.render('data/5a,4a景区占比及数量-饼图.html')
    print("\n5a,4a景区占比及数量-饼图.html文件生成成功,可以使用浏览器打开哦")

if __name__=='__main__':
    top_10_echart()
