# """
# 抓取
# 解析
# 存储
# """
import re
import ast
from urllib import parse
from datetime import datetime

import requests
from scrapy import Selector

from CSDN_spider.models import *

domain = "https://bbs.csdn.net"


def get_nodes_json():
    left_menu_text = requests.get("https://bbs.csdn.net/dynamic_js/left_menu.js?csdn").text
    print(left_menu_text)
    node_str_match = re.search(" forumNodes: (.*])", left_menu_text)  # 贪婪匹配，行末尾
    if node_str_match:
        nodes_str = node_str_match.group(1).replace("null", "None")
        nodes_list = ast.literal_eval(nodes_str)  # 转换为列表
        return nodes_list
    return []


url_list = []


def process_nodes_list(node_list):
    # 将JS的格式提取出url到list中
    for item in node_list:
        if "url" in item:
            if item["url"]:
                url_list.append(item["url"])
            if "children" in item:
                process_nodes_list(item["children"])


def get_level1_list(nodes_list):
    level1_url = []
    for item in nodes_list:
        if "url" in item and item["url"]:
            level1_url.append(item["url"])
    return level1_url


def get_last_urls():
    # 获取最终需要抓取的url
    nodes_list = get_nodes_json()
    process_nodes_list(nodes_list)
    level1_url = get_level1_list(nodes_list)
    last_url = []
    for url in url_list:
        if url not in level1_url:
            last_url.append(url)
    all_urls = []
    for url in url_list:
        all_urls.append(parse.urljoin(domain, url))
        all_urls.append(parse.urljoin(domain, url + "/recommend"))
        all_urls.append(parse.urljoin(domain, url + "/closed"))
    return all_urls


def parse_list(url):
    res_text = requests.get(url).text
    sel = Selector(text=res_text)
    all_trs = sel.xpath("//table[@class='forums_tab_table']//tr")[2:]  # 从第二个开始，tbody
    for tr in all_trs:
        topic = Topic()

        if tr.xpath(".//td[1]/span/text()").extract():
            status = tr.xpath(".//td[1]/span/text()").extract()[0]
            topic.status = status
        if tr.xpath(".//td[2]/em/text()").extract():
            score = tr.xpath(".//td[2]/em/text()").extract()[0]
            topic.score = score
        if tr.xpath(".//td[3]/a[2]/@href").extract():
            topic_url = parse.urljoin(domain, tr.xpath(".//td[3]/a[2]/@href").extract()[0])
            topic.id = int(topic_url.split("/")[-1])
        if tr.xpath(".//td[3]/a/text()").extract():
            topic_title = tr.xpath(".//td[3]/a/text()").extract()[0]
            topic.title = topic_title
        if tr.xpath(".//td[4]/a/@href").extract():
            author_url = parse.urljoin(domain, tr.xpath(".//td[4]/a/@href").extract()[0])
            author_id = author_url.split("/")[-1]
            topic.author = author_id
        if tr.xpath(".//td[4]/em/text()").extract():
            create_time_str = tr.xpath(".//td[4]/em/text()").extract()[0]
            create_time = datetime.strptime(create_time_str, "%Y-%m-%d %H:%M")
            topic.create_time = create_time
        if tr.xpath(".//td[5]/span/text()").extract():
            answer_info = tr.xpath(".//td[5]/span/text()").extract()[0]
            answer_nums = answer_info.split("/")[0]
            click_nums = answer_info.split("/")[1]
            topic.answer_nums = answer_nums
            topic.click_nums = click_nums
        if tr.xpath(".//td[6]/em/text()").extract():
            last_time_str = tr.xpath("//td[6]/em/text()").extract()[0]
            last_time = datetime.strptime(last_time_str, "%Y-%m-%d %H:%M")  # 字符串格式转换为时间格式
            topic.last_answer_time = last_time

        existed_topics = Topic.select().where(Topic.id == topic.id)
        if existed_topics:
            topic.save()
        else:
            topic.save(force_insert=True)

        # parse_topic(topic_url)
        parse_author(author_url)
    #
    # next_page = sel.xpath("//a[@class='pageliststy next_page']/@href").extract()
    # if next_page:
    #     next_url = parse.urljoin(domain, next_page[0])
    #     parse_list(next_url)


def parse_topic(url):
    # 获取帖子的详情以及帖子的回复
    topic_id = url.split("/")[-1]
    res_text = requests.get(url).text
    sel = Selector(text=res_text)
    all_divs = sel.xpath("//div[starts-with(@id,'post-')]")
    topic_item = all_divs[0]
    content = topic_item.xpath(".//div[@class='post_body post_body_min_h']").extract()[0]
    praised_nums = topic_item.xpath(".//label[@class='red_praise digg d_hide']//em/text()").extract()[0]
    jtl_str = topic_item.xpath(".//div[@class='close_topic']/text()").extract()[0]
    jtl = 0
    jtl_match = re.search("(\d+)%",jtl_str)
    if jtl_match:
        jtl = int(jtl_match.group(1))

    existed_topics = Topic.select().where(Topic.id == topic_id)
    if existed_topics:
        topic = existed_topics[0]
        topic.content = content
        topic.jtl = jtl
        topic.praised_nums = praised_nums
        topic.save()

    for answer_item in all_divs[1:]:
        answer = Answer()
        answer.topic_id = topic_id
        author_info = answer_item.xpath(".//div[@class='nick_name']/a[1]/@href").extract()[0]
        author_id = author_info.split("/")[-1]
        create_time = answer_item.xpath(".//label[@class='date_time']/text()").extract()[0]
        create_time = datetime.strptime(create_time, "%Y-%m-%d %H:%M:%S")
        answer.author = author_id
        answer.create_time = create_time
        praised_nums = topic_item.xpath(".//label[@class='red_praise digg d_hide']//em/text()").extract()[0]
        praised_nums_1 = praised_nums.split(' ')[-1]
        answer.parised_nums = int(praised_nums_1)
        content = topic_item.xpath(".//div[@class='post_body post_body_min_h']").extract()[0]
        answer.content = content

        answer.save()

    next_page = sel.xpath("//a[@class='pageliststy next_page']/@href").extract()
    if next_page:
        next_url = parse.urljoin(domain, next_page[0])
        parse_topic(next_url)


def parse_author(url):
    # 获取用户的详情
    headers = {
        'User-Agent':'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'
    }
    res_text = requests.get(url,headers = headers).text
    sel = Selector(text=res_text)
    original_nums = sel.xpath("//*[@class='me_chanel_det_item access'][1]/a/span/text()").extract()[-1]
    rate = sel.xpath("/html/body/div[2]/div[1]/div[3]/div[3]/span/text()").extract()



if __name__ == "__main__":
    last_urls = get_last_urls()  # 获取所有的URL
    for url in last_urls:
        parse_list(url)
    print(last_urls)

