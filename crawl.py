#导入模块123
import pandas as pd
import numpy as np
import requests
import os
import shutil
import datetime
import csv
import time


begin_time=time.time()


#读取数据
new_csv = pd.read_csv('https://cdn.jsdelivr.net/gh/qingfeng5365/my/csv/new.csv',low_memory = False)
old_csv = pd.read_csv('https://cdn.jsdelivr.net/gh/qingfeng5365/my/csv/old.csv',low_memory = False)
#创建DataFrame
new_df = pd.DataFrame(new_csv)
old_df = pd.DataFrame(old_csv)
#空值处理
new_df.fillna(0, inplace = True)
old_df.fillna(0, inplace = True)
#生成字典
new_back = dict(zip(new_df['room'],new_df['back']))
new_pro = dict(zip(new_df['room'],new_df['pro']))
old_back = dict(zip(old_df['room'],old_df['back']))
old_pro = dict(zip(old_df['room'],old_df['pro']))


#生成文件夹
if(not os.path.exists("image")):
    for i in new_back.keys():
        os.makedirs("image/new/"+i+"/back")
        os.makedirs("image/new/"+i+"/pro")
    for i in old_back.keys():
        os.makedirs("image/old/"+i+"/back")
        os.makedirs("image/old/"+i+"/pro")
#清空日志文件
with open('error.csv',mode='w',encoding='utf-8',newline='') as f:  
    f.truncate()

    
#爬取图片
def crawling (url,path):
    resp=requests.get(url,timeout=0.5)
    with open(path,'wb')as f:
        f.write(resp.content)
    resp.close()
#异常记录
def error_log(room,url,fname,pos):
    with open('error.csv',mode='a',encoding='utf-8',newline='') as f:
        csv_writer=csv.writer(f)
        csv_writer.writerow([room,pos,url,fname])
    
    
for room,ip in old_back.items():
    if ip:
        url="http://admin:12345@"+ip+"/Streaming/channels/1/picture"
        fname = datetime.datetime.now().strftime('%F %T').replace(":","-").replace(" ", "_")
        path="image/old/"+room+"/back/"+fname+".jpg"
        try:
            crawling(url,path)
        except:
            error_log(room,url,fname,"back")
for room,ip in old_pro.items():
    if ip:
        url="http://admin:12345@"+ip+"/Streaming/channels/1/picture"
        fname = datetime.datetime.now().strftime('%F %T').replace(":","-").replace(" ", "_")
        path="image/old/"+room+"/pro/"+fname+".jpg"
        try:
            crawling(url,path)
        except:
            error_log(room,url,fname,"pro")
            
            
end_time=time.time()
print(end_time-begin_time)
