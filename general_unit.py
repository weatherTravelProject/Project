"""
@File:general_unit.py
@Author:Yuying
@Date:2020/11/07
"""
import requests
import traceback
import pandas as pd
import json
import os

def get_content(url):
    # 输入url
    # 输出response（txt）
    try:
        header='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
        response=requests.get(url,header,timeout=30)
        response.raise_for_status()
        response.encoding=response.apparent_encoding
        print('爬取成功')
        return response.text
    except Exception as e:
        print('错误类型是:',e.__class__.__name__)
        print('错误明细为:',e)
        traceback.print_exc()

class save_data_as_json(object): #已优化(此形式输出不太直观)
    def save_file(self, path, item):
        item=json.dumps(item)#dumps将字典形式的数据转化为字符串
        try:
            if not os.path.exists(path):
                with open(path,'w',encoding='utf-8')as f:
                    f.write(item+"\n")
                    print("写入{}到{}成功".format(item.name,path))
            else:
                with open(path,'a',encoding='utf-8')as f:
                    f.write(item + "\n")
                    print("写入{}到{}成功".format(item.name,path))
        except Exception as e:
            print("错误类型为：", e.__class__.__name__)
            print("错误详情为：", e)
            traceback.print_exc()

"""   #保存为csv格式文件（有误）
def data_save:
  with open('travel_list.csv','w',newline='') as travel_list_csv:
       fieldnames=['城市','景点信息链接']
       w=csv.DictWriter(travel_list_csv,fieldnames=fieldnames)
       w.writeheader()
       w.writerows(travel_list)
       for key,value in travel_list.items():
            print(key, value)
"""
#参考csv官方说明https://docs.python.org/zh-cn/3.7/library/csv.html

def data_save(data,name):   #默认数据存储在当前目录下
    df=pd.DataFrame(data)
    print(df)
    df.to_csv(name)

if __name__=="__main__":
   url="https://travel.qunar.com/place/"
   html=get_content(url)
   print(html)