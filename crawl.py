#导入模块
import pandas as pd
import requests
import os
import datetime
import csv
import time
from io import StringIO
from requests.auth import HTTPDigestAuth
from concurrent.futures import ThreadPoolExecutor


#线程池new
def new(ip,room,pos):
    url=f"http://{ip}/cgi-bin/snapshot.cgichannel=1"
    fname = datetime.datetime.now().strftime('%F %T').replace(":","-").replace(" ", "_")
    try:
        with requests.get(url,auth=HTTPDigestAuth("admin","mzdx1234")) as resp: 
            if (resp.status_code!=200):
                with open('error_code.csv',mode='a',encoding='utf-8',newline='') as f:
                    csv_writer=csv.writer(f)
                    csv_writer.writerow([room,pos,resp.status_code,url,fname])
            else:
                path="image/new/"+room+"/"+pos+"/"+fname+".jpg"
                with open(path,'wb')as f:
                    f.write(resp.content)
    except:
        with open('error_timeout.csv',mode='a',encoding='utf-8',newline='') as f:
            csv_writer=csv.writer(f)
            csv_writer.writerow([room,pos,url,fname])

#线程池old
def old(ip,room,pos):
    url=f"http://admin:12345@{ip}/Streaming/channels/1/picture"
    fname = datetime.datetime.now().strftime('%F %T').replace(":","-").replace(" ", "_")
    try:
        with requests.get(url,timeout=1) as resp: 
            if (resp.status_code!=200):
                with open('error_code.csv',mode='a',encoding='utf-8',newline='') as f:
                    csv_writer=csv.writer(f)
                    csv_writer.writerow([room,pos,resp.status_code,url,fname])
            else:
                path="image/old/"+room+"/"+pos+"/"+fname+".jpg"
                with open(path,'wb')as f:
                    f.write(resp.content)
    except:
        with open('error_timeout.csv',mode='a',encoding='utf-8',newline='') as f:
            csv_writer=csv.writer(f)
            csv_writer.writerow([room,pos,url,fname])
            
if __name__=="__main__":
    
    t1=time.time()
    #读取数据
    url1='https://api.fernvenue.com/gh/qingfeng5365/my/master/csv/new.csv'
    url2='https://api.fernvenue.com/gh/qingfeng5365/my/master/csv/old.csv'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'}
    s1=requests.get(url1,headers=headers).text
    s2=requests.get(url2,headers=headers).text
    new_csv = pd.read_csv(StringIO(s1))
    old_csv = pd.read_csv(StringIO(s2))
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
    with open('error_timeout.csv',mode='w',encoding='utf-8',newline='') as f:  
        f.truncate()
    with open('error_code.csv',mode='w',encoding='utf-8',newline='') as f:  
        f.truncate()

    #线程池
    with ThreadPoolExecutor(30) as t:
        for room,ip in old_back.items():
            if ip:
                t.submit(old,ip,room,"back")
        for room,ip in old_pro.items():
            if ip:
                t.submit(old,ip,room,"pro")
        for room,ip in new_back.items():
            if ip:
                t.submit(new,ip,room,"back")
        for room,ip in new_pro.items():
            if ip:
                t.submit(new,ip,room,"pro")
    t2=time.time()
    print(t2-t1)
