import threading
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep,ctime
import os,sys
from multiprocessing.pool import ThreadPool

headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}

def book_info(html_source):
    html = BeautifulSoup(html_source, features="lxml")
    book_header = html.find(class_="book-header")
    book_name = book_header.h1.contents[0]
    host = 'https://www.mhzzz.xyz/'
    img = book_header.p.img
    icon_url = host + img['src']
    return book_name,icon_url

def get_chapter_images_url(html_source):
    html = BeautifulSoup(html_source, features="lxml")
    p = html.find(id='imgList')
    img_list = p.select('img')
    host = 'https://www.mhzzz.xyz/'
    chapter_images_url = []
    for i in img_list:
        url = host + i['src']
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
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    sleep(1)
    alert = driver.switch_to_alert()
    alert.accept()
    items = driver.find_elements_by_xpath("//div[@id='chapter-list']/div/div/a")
    book_name, icon_url = book_info(driver.page_source)
    html = BeautifulSoup(driver.page_source, features="lxml")
    list_items = html.find_all(class_="list-item")
    if not os.path.exists(book_name):
        os.makedirs(book_name)
        temp = [icon_url]
        download_image(icon_url,temp,book_name)

    items[chapter_start-1].click()

    for i in range(chapter_start,chapter_sum+1):
        try:
            next_chapter = driver.find_element_by_link_text('下一話')
        except:
            break
        chapter_dir = ('./%03d ' %  i) + list_items[i-1].a.div.div.text
        chapter_dir = os.path.join(book_name,chapter_dir)
        if not os.path.exists(chapter_dir):
            os.makedirs(chapter_dir)
        chapter_images_url = get_chapter_images_url(driver.page_source)        
        image_list = download_image_thread(chapter_images_url, out_dir=chapter_dir, num_processes=8, remove_bad=True, Async=True)
        next_chapter.click()
    driver.quit()

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