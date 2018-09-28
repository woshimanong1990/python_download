#coding:utf-8
import asyncio
import sys
import time
import os
import cgi
import re

from urllib import parse
from urllib.parse import urlparse, unquote_plus

file_name_pattern = re.compile(r"utf|UTF-8'\s+'")
import aiohttp
def get_file_name(content_disposition):
    _, params = cgi.parse_header(content_disposition)
    if "filename" in params:
        return params["filename"]
    elif "FILENAME" in params:
        return params["FILENAME"]
    elif "filename*" in params:
        return re.split("utf-8'\s+'", params['filename*'], 1, flags=re.IGNORECASE)[1]
    elif "FILENAME*" in params:
        return re.split("utf-8'\s+'", params['FILENAME*'], 1, flags=re.IGNORECASE)[1]
    else:
        return None
    


async def fetch(session, url, startpos, endpos, filename):
    headers = {
        "Range":"bytes=%s-%s"%(startpos,endpos),
        "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-encoding":"gzip, deflate, br",
        "accept-language":"zh-CN,zh;q=0.9",
        "upgrade-insecure-requests":"1",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
    }
    print("fetch...", startpos, endpos)
    async with session.get(url, headers=headers) as response:
        with open(filename, 'rb+') as fd:
            fd.seek(startpos)
            while True:
                chunk = await response.content.read(1024)
                if not chunk:
                    break
                fd.write(chunk)
        

async def main(url, thread_num):
    
    #获取文件的大小和文件名
    urlobj = urlparse(url)
    filename = ""
    start = 0
    end = -1
    step = 0
    tasks = []
    headers = {
        "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-encoding":"gzip, deflate, br",
        "accept-language":"zh-CN,zh;q=0.9",
        "upgrade-insecure-requests":"1",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
    }
    #https://www.cnblogs.com/momoxingchen/p/6493317.html
    async with aiohttp.ClientSession() as session:
        async with session.head(url, headers=headers) as response:
            headers_content = response.headers
            print("headers_content", headers_content)
            if "Content-Length" not in headers_content:
                raise Exception("can't get file size")
            filename = urlobj.path.rsplit('/',1)[1]
            if 'Content-Disposition' in headers_content:
                tmp_file_name = get_file_name(headers_content["Content-Disposition"])
                if tmp_file_name is not None and tmp_file_name:
                    filename = tmp_file_name
            filesize = int(headers_content["Content-Length"])
            step = filesize // thread_num
            print("%s filesize:%s"%(filename,filesize))
    with open(filename,'w') as tempf:
        tempf.seek(0)
        tempf.write("hello")

    async with aiohttp.ClientSession() as session:
        while end < filesize -1:
            start = end +1
            end = start + step -1
            print("start:end:", start,end)
            if end > filesize:
                end = filesize
            task = asyncio.ensure_future(fetch(session,url,start, end, filename))
            tasks.append(task)
        await asyncio.gather(*tasks)
         
    

if __name__ == "__main__":
    url = "https://res.youth.cn/article_201809_28_28z_5badd046ee52a.jpg"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(url, 2))
   