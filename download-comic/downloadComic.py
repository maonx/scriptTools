import os
from importlib import import_module
import requests
from bs4 import BeautifulSoup
import sys

def main(url, chapter_start, chapter_sum):
    r = requests.get(url)
    html = BeautifulSoup(r.content, features="lxml")
    book_name,icon_url = book_info(html)
    url_list, title_list = get_chapters(html)
    # print(title_list)
    for i in range(chapter_start-1, chapter_start + chapter_sum -1):
        chapter_dir = os.path.join(book_name, title_list[i])



if __name__ == '__main__':
    MAX_CHAPTER_NUM = 1000
    if len(sys.argv) == 1:
        print("usage:download-comic.py URL [chapter_sum] [start_chapter_num]")
    else :
        url = sys.argv[1]
        if 'hm.top/' in url:
            from comicsite.hmtop import *
            # book_info = import_module('site.hmtop.book_info')
            # get_chapter_images_url = import_module('site.hmtop.get_chapter_images_url')
            # get_chapter_url = import_module('site.hmtop.get_chapter_url')
        else:
            book_info = import_module('mhzzz.book_info')
            get_chapter_images_url = import_module('mhzzz.get_chapter_images_url')
            get_chapter_url = import_module('mhzzz.get_chapter_url')
        chapter_sum = MAX_CHAPTER_NUM
        chapter_start = 1
        if len(sys.argv) == 3 : chapter_start = int(sys.argv[2])
        if len(sys.argv) == 4 : chapter_sum = int(sys.argv[3])
        main(url,chapter_start,chapter_sum)