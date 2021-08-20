import threading
from threading import Thread
from queue import Queue
import queue 
import time
import requests
import os
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool
import PIL.Image as Image
from io import BytesIO
import numpy as np

headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}
# producer_queue = queue.Queue()
# thread_exit_Flag = False
# queue_lock = threading.Lock() 

all_url_list = []
with open('url.txt','r') as f:
    content = f.readlines()
    for i in content:
        i = i.strip('\n')
        all_url_list.append(i)

def get_chapter_images_url(chapter_url):
    r = requests.get(chapter_url, headers=headers)
    html = BeautifulSoup(r.text, features="lxml")
    p = html.find(id='imgList')
    img_list = p.select('img')
    host = 'https://www.mhzzz.xyz/'
    chapter_images_url = []
    page = 1
    for i in img_list:
        url = host + i['src']
        # chapter_images_url.append({'page':page,'url':url})
        chapter_images_url.append(url)
        page +=1
    return chapter_images_url

# def download_image(url,image_name):
#     r = requests.get(url)
#     with open(image_name, 'wb') as f:
#         f.write(r.content)    

# def download_image(url, our_dir):
#     basename = os.path.basename(url)
#     image_name = os.path.join(our_dir, basename)
#     r = requests.get(url)
#     with open(image_name, 'wb') as f:
#         f.write(r.content)    
#     print("download image successfully:{}".format(url))

def download_image(url, url_list, out_dir):
    image_name = "%03d.jpg" % (url_list.index(url) + 1)
    image_name = os.path.join(out_dir, image_name)
    if not os.path.exists(image_name):
        r = requests.get(url,headers=headers)
        with open(image_name, 'wb') as f:
            f.write(r.content)    
        print("download image successfully:{}".format(image_name))

# def download_image(url, our_dir):
#     '''
#     根据url下载图片
#     :param url:
#     :return: 返回保存的图片途径
#     '''
#     basename = os.path.basename(url)
 
#     try:
#         res = requests.get(url)
#         if res.status_code == 200:
#             print("download image successfully:{}".format(url))
#             filename = os.path.join(our_dir, basename)
#             with open(filename, "wb") as f:
#                 content = res.content
#                 # 使用Image解码为图片
#                 # image = Image.open(BytesIO(content))
#                 # image.show()
#                 # 使用opencv解码为图片
#                 content = np.asarray(bytearray(content), dtype="uint8")
#                 # image = cv2.imdecode(content, cv2.IMREAD_COLOR)
#                 # cv2.imshow("Image", image)
#                 # cv2.waitKey(1000)
#                 # f.write(content)
#                 # time.sleep(2)
#             return filename
#     except Exception as e:
#         print(e)
#         return None
#     print("download image failed:{}".format(url))
#     return None

def download_image_thread(url_list, out_dir, num_processes, remove_bad=False, Async=True):
    '''
    多线程下载图片
    :param url_list: image url list
    :param out_dir:  保存图片的路径
    :param num_processes: 开启线程个数
    :param remove_bad: 是否去除下载失败的数据
    :param Async:是否异步
    :return: 返回图片的存储地址列表
    '''
    # 开启多线程
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    pool = ThreadPool(processes=num_processes)
    thread_list = []
    for image_url in url_list:
        if Async:
            out = pool.apply_async(func=download_image, args=(image_url, url_list, out_dir))  # 异步
        else:
            out = pool.apply(func=download_image, args=(image_url, url_list))  # 同步
        thread_list.append(out)
 
    pool.close()
    pool.join()
    # 获取输出结果
    image_list = []
    if Async:
        for p in thread_list:
            image = p.get()  # get会阻塞
            image_list.append(image)
    else:
        image_list = thread_list
    if remove_bad:
        image_list = [i for i in image_list if i is not None]
    return image_list

def doTask():
    while not thread_exit_Flag:
        queue_lock.acquire() 
        if producer_queue.empty():
            queue_lock.release()
            time.sleep(1)
            continue
        task = producer_queue.get()
        image_name = "%03d.jpg" % task['page']
        download_image(task['url'], image_name)
        print("download %s" % image_name)
        print("thread %d consumer download task %d" % (threading.get_ident(), task['page']))
        queue_lock.release()    
    print("thread %d exit" % (threading.get_ident()))    
 
# for i in all_url_list:
#     producer_queue.put(i)
# num_threads = 10
# threads_list = []
# for i in range(num_threads):
#     # Set up some threads to dotask
#     consumer = Thread(target = doTask)
#     consumer.start()
#     threads_list.append(consumer)
 
# # Wait for the queue to empty 
# while not producer_queue.empty(): 
#     pass
 
# # Notify threads it's time to exit 
# thread_exit_Flag = True
 
# # Wait for all threads to complete 
# for t in threads_list: 
#     t.join() 
# print("exit")
# url_list = get_chapter_images_url("https://www.mhzzz.xyz/play?linkId=533947&bookId=527&key=E0xvs92ujPnpL36wtg5U6w==") 
# our_dir = "."
# startTime = time.time()
for i in all_url_list:
    chapter = all_url_list.index(i) + 191
    chapter_dir = './%03d' %  chapter
    if not os.path.exists(chapter_dir):
        os.makedirs(chapter_dir)
    chapter_images_url = get_chapter_images_url(i)
    image_list = download_image_thread(chapter_images_url, out_dir=chapter_dir, num_processes=8, remove_bad=True, Async=True)
# endTime = time.time()
# consumeTime = endTime - startTime
# print("程序运行时间：" + str(consumeTime) + " 秒")
# print(image_list)