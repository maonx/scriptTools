import os
import requests

headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}

def del_char(str):
    # 删除文件名中无法命名的字符
    DELETE_CHAR = '\:*?"<>|'
    for i in DELETE_CHAR:
        if str.find(i) != -1:
            str = str.replace(i,'')
    return str

def download_image(url, image_name):
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
    # image_list = []
    # if Async:
    #     for p in thread_list:
    #         image = p.get()  # get会阻塞
    #         image_list.append(image)
    # else:
    #     image_list = thread_list
    # if remove_bad:
    #     image_list = [i for i in image_list if i is not None]
    # return image_list

