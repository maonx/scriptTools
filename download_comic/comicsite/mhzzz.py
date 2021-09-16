import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep,ctime
import os,sys
sys.path.append('..')
from util import *

def book_info(url):
    r = requests.get(url)
    html = BeautifulSoup(r.content, features="lxml")
    book_header = html.find(class_="book-header")
    book_name = del_char(book_header.h1.contents[0])
    host = 'https://www.mhzzz.xyz/'
    img = book_header.p.img
    icon_url = host + img['src']
    icon_name = os.path.join(book_name,'000_cover.jpg')
    if not os.path.exists(book_name):
        os.makedirs(book_name)
    if not os.path.exists(icon_name):
        download_image(icon_url, icon_name)

    return book_name,icon_url

def get_chapter_images_url(url):
    r = requests.get(url)
    html = BeautifulSoup(r.content, features="lxml")
    p = html.find(id='imgList')
    img_list = p.select('img')
    host = 'https://www.mhzzz.xyz/'
    chapter_images_url = []
    for i in img_list:
        url = host + i['src']
        chapter_images_url.append(url)
    return chapter_images_url

def get_chapters(url, chapter_start, chapter_sum):
    options = webdriver.ChromeOptions()
    # 不加载图片，加速网址获取
    prefs = {"profile.managed_default_content_settings.images":2}
    options.add_experimental_option("prefs",prefs)

    # 不显示logging
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    sleep(1)
    alert = driver.switch_to_alert()
    alert.accept()
    items = driver.find_elements_by_xpath("//div[@id='chapter-list']/div/div/a")
    title_list = []
    for i in items:
        item = i.find_element_by_class_name('cell-title')
        text = del_char(item.text)
        title_list.append(text)

    if chapter_sum > len(items):
        chapter_sum = len(items)

    items[chapter_start-1].click()

    url_list = []
    for i in range(chapter_sum):
        url_list.append(i)
    for i in range(chapter_start-1, chapter_start + chapter_sum -1):
        try:
            next_chapter = driver.find_element_by_link_text('下一話')
        except:
            break
        url_list[i] = driver.current_url
        next_chapter.click()
    driver.quit()
    return url_list, title_list