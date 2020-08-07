import json
import logging
import requests
import os
import time

from multiprocessing import Queue
from concurrent.futures import ThreadPoolExecutor
# from logging_test.user_log import Userlog
# 创建队列
queue_list = Queue()
# log = Userlog()
# logger = log.get_log()

class Userlog(object):
    def __init__(self):
        self.logger = logging.getLogger()  # 实例化对象
        self.logger.setLevel(logging.DEBUG)  # 设置一个等级
        # 控制台输出日志
        # consle = logging.StreamHandler() # 输入输出流
        # logger.addHandler(consle) # 添加流
        # logger.debug("info")
        # 文件名字
        base_dir = os.path.dirname(os.path.abspath(__file__))
        log_dir = os.path.join(base_dir, "logs")
        log_file = time.strftime("%Y-%m-%d-%H-%M-%S") + ".log"
        log_name = log_dir + "/" + log_file
        print(log_name)
        if os.path.exists(log_dir):
            pass
        else:
            os.makedirs(log_dir)
        # 文件输出日志
        self.file_handle = logging.FileHandler(log_name, 'a', encoding="utf-8")
        # 日志的格式化输出
        formatter = logging.Formatter(
            '%(asctime)s %(filename)s--> %(funcName)s %(levelno)s: %(levelname)s -----> %(message)s')
        self.file_handle.setFormatter(formatter)
        self.logger.addHandler(self.file_handle)
        # logger.debug("teste1234")

    def get_log(self):
        return self.logger

    def close_handle(self):
        self.file_handle.close()
        self.logger.removeHandler(self.file_handle)
def header_requests(url, data):
    header = {
        "client": "4",
        "version": "6922.2",
        "device": "SM-N960F",
        "sdk": "22,5.1.1",
        "imei": "355757705783419",
        "channel": "zhuzhan",
        # "mac":"00:E0:4C:68:34:A5",
        "resolution": "1600*900",
        "dpi": "2.0",
        # "android-id":"d6f9a8a425956600",
        # "pseudo-id":"8a425956600d6f9a",
        "brand": "samsung",
        "scale": "2.0",
        "timezone": "28800",
        "language": "zh",
        "cns": "2",
        "carrier": "CMCC",
        # "imsi":"460077015834165",
        "user-agent": "Mozilla/5.0 (Linux; Android 5.1.1; SM-N960F Build/JLS36C; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36",
        "reach": "1",
        "newbie": "0",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "Keep-Alive",
        # "Cookie":"duid=65269540",
        "Host": "api.douguo.net",
        "Content-Length": "89",
    }
    response = requests.post(url=url, headers=header, data=data)
    return response


def handler_index():
    url = 'http://api.douguo.net/recipe/flatcatalogs'
    data = {
        "client": "4",
        "_session": "1595080076866355757705783419",
        "v": "1595070788",
        "_vs": "2305",
    }
    response = header_requests(url=url, data=data)
    # print(response.text)
    index_json_dict = json.loads(response.text)  # 转换成为字典样式
    for index_item in index_json_dict['result']['cs']:
        for index_item_1 in index_item['cs']:
            for item in index_item_1['cs']:
                # print(item)
                data_2 = {
                    "client": "4",
                    "_session": "1595075769192355757705783419",
                    "keyword": item['name'],
                    "order": "0",
                    "_vs": "400",
                }
                queue_list.put(data_2)


def handle_caipu_list(data):
    print("现在检索的食材是：", data['keyword'])
    caipu_list_url = 'http://api.douguo.net/recipe/v2/search/0/20'
    caipu_list_response = header_requests(url=caipu_list_url, data=data)
    caipu_list_response_dict = json.loads(caipu_list_response.text)
    caipu_info = {}  # 创建一个空字典，将数据都放到该空字典中
    caipu_info['shicai'] = data['keyword']
    for item in caipu_list_response_dict['result']['list']:
        if item['type'] == 13:
            caipu_info['author'] = item['r']['an']
            caipu_info['caipu_id'] = item['r']['id']
            caipu_info['caipu_name'] = item['r']['n']
            caipu_info['describe'] = item['r']['cookstory'].replace('\n', '')
            caipu_info['materials'] = item['r']['major']
            detail_url = 'http://api.douguo.net/recipe/detail/' + str(caipu_info['caipu_id'])
            detail_data = {
                "client": "4",
                "_session": "1595148703712355757705783419",
                "author_id": "0",
                "_vs": "0",
            }
            detail_response = header_requests(url=detail_url, data=detail_data)
            detail_response_dict = json.loads(detail_response.text)
            caipu_info['ciapu_tips'] = detail_response_dict['result']['recipe']['tips']
            caipu_info['ciapu_cookstep'] = detail_response_dict['result']['recipe']['cookstep']
            print(caipu_info)  # 转换成json格式
            logger.debug("this is test")
            log.close_handle()
            # (1)json.dumps()函数是将一个Python数据类型列表进行json格式的编码（可以这么理解，json.dumps()函数是将字典转化为字符串）
            # (2)json.loads()函数是将json格式数据转换为字典（可以这么理解，json.loads()函数是将字符串转化为字典
        else:
            continue


if __name__ == "__main__":
    log = Userlog()
    logger = log.get_log()
    handler_index()
    pool = ThreadPoolExecutor(max_workers=20)
    while queue_list.qsize()>0:
        pool.submit(handle_caipu_list,queue_list.get())



    # handle_caipu_list(queue_list.get())  # Queue.get():获取队列中的一条消息，然后将其从列队中移除，可传参超时时长。
    # print(queue_list.qsize()) #qsize,数据量
