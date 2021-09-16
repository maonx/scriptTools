import os
from importlib import import_module
import requests
from bs4 import BeautifulSoup
import sys

def main(url, chapter_start, chapter_sum):
    book_name,icon_url = book_info(url)
    url_list, title_list = get_chapters(url, chapter_start, chapter_sum)
    for i in range(chapter_start-1, chapter_start + chapter_sum -1):
        if i >= len(title_list):
            break
        chapter_dir = ('%03d ' % (i+1)) + title_list[i]
        chapter_dir = os.path.join(book_name, chapter_dir)
        if not os.path.exists(chapter_dir):
            os.makedirs(chapter_dir)
        chapter_images_url = get_chapter_images_url(url_list[i])
        download_image_thread(chapter_images_url, chapter_dir, 8)



if __name__ == '__main__':
    MAX_CHAPTER_NUM = 1000
    if len(sys.argv) == 1:
        print("usage:download-comic.py URL [chapter_start_number] [download_chapter_sum]")
    else :
        url = sys.argv[1]
        if 'hm.top/' in url:
            from comicsite.hmtop import *
        else:
            from comicsite.mhzzz import *
        chapter_sum = MAX_CHAPTER_NUM
        chapter_start = 1
        if len(sys.argv) == 3 : chapter_start = int(sys.argv[2])
        if len(sys.argv) == 4 : chapter_sum = int(sys.argv[3])
        main(url,chapter_start,chapter_sum)