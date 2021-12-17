#导入模块
import pandas as pd
import numpy as np
import requests
import os
import shutil
import datetime
import csv
import time
import asyncio
import aiohttp
import aiofiles


#异常记录
async def error_log(room,url,fname,pos):
    async with aiofiles.open('error.csv',mode='a',encoding='utf-8',newline='') as f:
        csv_writer=csv.writer(f)
        await csv_writer.writerow([room,pos,url,fname])
            
#爬取图片
async def crawling (room,url,fname,path,pos):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url,timeout=1) as resp:
                async with aiofiles.open(path,'wb')as f:
                    await f.write(await resp.content.read())
    except:
        await error_log(room,url,fname,pos)
            

async def main():
    
    tasks1=[]
    for room,ip in old_back.items():
        if ip:
            url="http://admin:12345@"+ip+"/Streaming/channels/1/picture"
            fname = datetime.datetime.now().strftime('%F %T').replace(":","-").replace(" ", "_")
            path="image/old/"+room+"/back/"+fname+".jpg"
            t1=asyncio.create_task(crawling(room,url,fname,path,"back"))
            tasks1.append(t1)
    await asyncio.wait(tasks1)
    
    tasks2=[]
    for room,ip in old_pro.items():
        if ip:
            url="http://admin:12345@"+ip+"/Streaming/channels/1/picture"
            fname = datetime.datetime.now().strftime('%F %T').replace(":","-").replace(" ", "_")
            path="image/old/"+room+"/pro/"+fname+".jpg"
            t2=asyncio.create_task(crawling(room,url,fname,path,"pro"))
            tasks2.append(t2)
    await asyncio.wait(tasks2)    
    
    
if __name__=="__main__":
    
    t1=time.time()
    
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
        
    await main()
    t2=time.time()
    print(t2-t1)