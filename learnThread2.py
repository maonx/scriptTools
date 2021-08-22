import threading
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep,ctime

headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}

url = "https://www.mhzzz.xyz/manhua/info/238773.html"

def fuc(url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    sleep(1)
    alert = driver.switch_to_alert()
    alert.accept()
    items = driver.find_elements_by_xpath("//div[@id='chapter-list']/div/div/a")
    # driver.quit()
    # print(len(items))
    for i in range(len(items)):
        if i == 0:
            items[i].click()
        else:
            driver.find_element_by_link_text('下一話').click()
        sleep(0.5)
        print(driver.current_url)
    driver.quit()

def fuc2(url, object):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    # sleep(1)
    alert = driver.switch_to_alert()
    alert.accept()
    object.click()
    print(driver.current_url)

# threads = []
# nloops = range(5)

# for i in nloops:
#     t = threading.Thread(target=fuc,
#         args=(url, i))
#     threads.append(t)

# for i in nloops:
#     threads[i].start()

# for i in nloops:
#     threads[i].join()

print("starting at: %s" % ctime())
fuc(url)
print("all Done at: %s" % ctime())