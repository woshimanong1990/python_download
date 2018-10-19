#! -coding:utf8 -*-
import threading
import sys
import time
import os
import multiprocessing
import time
import traceback
import datetime

import requests
from urllib.parse import urlparse

def show_process(percent, speed):
    end_char = "\r"
    if percent >= 1:
        end_char = "\n"
    bar_number = 100
    done_number = round(percent * bar_number) 
    done_char = "#" * done_number
    remain_char = "-" * (bar_number-done_number)
    process_bar = "[{done_char}{remain_char}] {percent}% speed:{speed}".format(done_char=done_char,
                                                                     remain_char=remain_char,
                                                                     speed=speed,
                                                                     percent="%0.2f" % (percent * 100)
                                                                     )
    print(process_bar, end=end_char)

def check_download_speed(file_size, queue):
    write_size = 0
    print("check_download_speed========") 
    while True:
        speed = 0
        current_time = time.time()
        while not queue.empty():
            item = queue.get(True)
            size = item.get("size", 0)
            at_time = item.get("time", current_time-10000)
            write_size += size
            if current_time - at_time > 1:
                break 
            speed += size
        print("check_download_speed running........") 
        percent = write_size/file_size
        try:  
            show_process(percent, speed)
        except Exception as e:
            print("show_process error", e)
        time.sleep(0.2)
        if percent >=1:
            time.sleep(2)
            os.kill(os.getpid(), 9)
            break


def download(url, startpos, endpos, filename, queue):
    try:
        with open(filename, 'rb+') as f:
            print("start downloading****")
            headers = {"Range":"bytes=%s-%s"%(startpos,endpos)}
            response = requests.get(url,headers=headers, stream=True)
            # res.text 是将get获取的byte类型数据自动编码，是str类型， res.content是原始的byte类型数据
            # 所以下面是直接write(res.content)
            f.seek(startpos)
            for data in response.iter_content(chunk_size=1024):
                f.write(data)
                queue.put({"time": time.time(), "size":len(data) })
                #print("write date", len(data))
            #print("-- download file:", startpos, len(res.content))
    except Exception as e:
        print("download error", e)
        traceback.print_exc()
def test(url, startpos, endpos, dup):
    print("test")
    fd = os.fdopen(dup,'rb+',-1)
    print(fd)
    time.sleep(2)
def main():
    url = "http://releases.ubuntu.com/18.04.1/ubuntu-18.04.1-desktop-amd64.iso?_ga=2.253642250.2068459485.1537842985-582867938.1537842985"
    #获取文件的大小和文件名
    urlobj = urlparse(url)
    filename = urlobj.path.rsplit('/',1)[1]
    filesize = int(requests.head(url).headers['Content-Length'])
    print("%s filesize:%s"%(filename,filesize))
    # queue = multiprocessing.Queue(10000)
    
    manager = multiprocessing.Manager()
    queue = manager.Queue(10000)

    process=multiprocessing.Process(target=check_download_speed, args=(filesize,queue))
    start = 0
    end = -1
    # 请空并生成文件
    with open(filename,'w') as tempf:
        tempf.seek(0)
        tempf.write("hello")

    # rb+ ，二进制打开，可任意位置读写
    cores = 4  #multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cores)
    step = filesize // cores
    print("step:", step)
    
        # 如果文件大小为11字节，那就是获取文件0-10的位置的数据。如果end = 10，说明数据已经获取完了。
    while end < filesize -1:
        start = end +1
        end = start + step -1
        print("start:end:", start,end)
        if end > filesize:
            end = filesize
        async_result = pool.apply_async(download,(url, start, end, filename, queue))
            # async_result.get(3600)
    
    pool.close()
    process.start()
    pool.join()
    # time.sleep(10)
    process.join()
    print("process join done")

if __name__ == "__main__":
    try:
       main()
    except KeyboardInterrupt as e:
       sys.exit(-1)
    