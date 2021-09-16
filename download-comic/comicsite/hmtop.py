import requests
from bs4 import BeautifulSoup
import os,sys
sys.path.append('..')
from util import *

def book_info(url):
    r = requests.get(url)
    html = BeautifulSoup(r.content, features="lxml")
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

def get_chapter_images_url(url):
    r = requests.get(url)
    html = BeautifulSoup(r.content, features="lxml")
    p = html.find(class_="comicpage")
    img_list = p.select('img')
    chapter_images_url = []
    for i in img_list:
        url = i['data-original']
        chapter_images_url.append(url)
    return chapter_images_url

def get_chapters(url, chapter_start, chapter_sum):
    r = requests.get(url)
    html = BeautifulSoup(r.content, features="lxml")
    host = 'http://www.92hm.top'
    detail_list = html.find(id="detail-list-select")
    items = detail_list.select('a')
    title_list = []
    url_list =[]
    for item in items:
        title_list.append(del_char(item.text))
        url_list.append(host + item['href'])
    return url_list, title_list

