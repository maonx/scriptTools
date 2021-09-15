import requests
from bs4 import BeautifulSoup
from time import sleep,ctime
import os,sys
sys.path.append('..')
from util import *

DELETE_CHAR = '\:*?"<>|'

def book_info(html):
    book_header = html.find(class_="banner_detail_form")
    book_name = del_char(book_header.h1.text)
    img = book_header.div.img
    icon_url = img['src']
    icon_name = os.path.join(book_name,'000_cover.jpg')
    if not os.path.exists(book_name):
        os.makedirs(book_name)
    if not os.path.exists(icon_name):
        download_image(icon_url, icon_name)
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

def get_chapters(html):
    host = 'http://www.92hm.top'
    detail_list = html.find(id="detail-list-select")
    items = detail_list.select('a')
    title_list = []
    url_list =[]
    for item in items:
        title_list.append(del_char(item.text))
        url_list.append(host + item['href'])
    return url_list, title_list

# def main(url, chapter_start = 1, chapter_sum = 1000):
#     r = requests.get(url)
#     book_name, icon_url = book_info(r.content)
#     html = BeautifulSoup(r.content, features="lxml")
#     detail_list = html.find(id="detail-list-select")
#     items = detail_list.select('a')

#     if not os.path.exists(book_name):
#         os.makedirs(book_name)
#         temp = [icon_url]
#         download_image(icon_url,temp,book_name)

#     count = len(items)
#     if chapter_sum > count :
#         chapter_sum = count
#     for i in range(chapter_start,chapter_sum+1):
#         chapter_dir = ('./%03d ' %  i) + items[i-1].text
#         for j in DELETE_CHAR:
#             if chapter_dir.find(j) != -1:
#                 chapter_dir = chapter_dir.replace(j, '')
#         chapter_dir = os.path.join(book_name,chapter_dir)
#         if not os.path.exists(chapter_dir):
#             os.makedirs(chapter_dir)
#         url2 = "http://www.92hm.top" + items[i-1]['href']
#         page_source = requests.get(url2)
#         chapter_images_url = get_chapter_images_url(page_source.content)
#         image_list = download_image_thread(chapter_images_url, out_dir=chapter_dir, num_processes=8, remove_bad=True, Async=True)

# if __name__ == "__main__":
#     MAX_CHAPTER_NUM = 1000
#     if len(sys.argv) == 1:
#         print("usage:download-comic.py URL [chapter_sum] [start_chapter_num]")
#     else :
#         chapter_sum = MAX_CHAPTER_NUM
#         chapter_start = 1
#         if len(sys.argv) == 3 : chapter_start = int(sys.argv[2])
#         if len(sys.argv) == 4 : chapter_sum = int(sys.argv[3])
#         main(sys.argv[1],chapter_start,chapter_sum)