import threading
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep,ctime
import os,sys
from multiprocessing.pool import ThreadPool

headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}

DELETE_CHAR = '\:*?"<>|'

def book_info(html_source):
    html = BeautifulSoup(html_source, features="lxml")
    # print(html)
    book_header = html.find(class_="banner_detail_form")
    book_name = book_header.h1.text
    img = book_header.div.img
    icon_url = img['src']
    return book_name,icon_url

def get_chapter_images_url(html_source):
    html = BeautifulSoup(html_source, features="lxml")
    p = html.find(class_="comicpage")
    img_list = p.select('img')
    chapter_images_url = []
    for i in img_list:
        url = i['data-original']
        chapter_images_url.append(url)
    return chapter_images_url

def download_image(url, url_list, out_dir):
    image_name = "%03d.jpg" % (url_list.index(url) + 1)
    image_name = os.path.join(out_dir, image_name)
    if not os.path.exists(image_name):
        r = requests.get(url,headers=headers)
        with open(image_name, 'wb') as f:
            f.write(r.content)    
        print("download image successfully:{}".format(image_name))

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

def main(url, chapter_start = 1, chapter_sum = 1000):
    r = requests.get(url)
    book_name, icon_url = book_info(r.content)
    html = BeautifulSoup(r.content, features="lxml")
    detail_list = html.find(id="detail-list-select")
    items = detail_list.select('a')

    if not os.path.exists(book_name):
        os.makedirs(book_name)
        temp = [icon_url]
        download_image(icon_url,temp,book_name)

    count = len(items)
    if chapter_sum > count :
        chapter_sum = count
    for i in range(chapter_start,chapter_sum+1):
        chapter_dir = ('./%03d ' %  i) + items[i-1].text
        for j in DELETE_CHAR:
            if chapter_dir.find(j) != -1:
                chapter_dir = chapter_dir.replace(j, '')
        chapter_dir = os.path.join(book_name,chapter_dir)
        if not os.path.exists(chapter_dir):
            os.makedirs(chapter_dir)
        url2 = "http://www.92hm.top" + items[i-1]['href']
        page_source = requests.get(url2)
        chapter_images_url = get_chapter_images_url(page_source.content)
        image_list = download_image_thread(chapter_images_url, out_dir=chapter_dir, num_processes=8, remove_bad=True, Async=True)

if __name__ == "__main__":
    MAX_CHAPTER_NUM = 1000
    if len(sys.argv) == 1:
        print("usage:download-comic.py URL [chapter_sum] [start_chapter_num]")
    else :
        chapter_sum = MAX_CHAPTER_NUM
        chapter_start = 1
        if len(sys.argv) == 3 : chapter_start = int(sys.argv[2])
        if len(sys.argv) == 4 : chapter_sum = int(sys.argv[3])
        main(sys.argv[1],chapter_start,chapter_sum)