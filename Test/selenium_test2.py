from selenium import webdriver
import time
from scrapy import Selector

# url = "http://caomudai.com/"
auth_url = "http://admin:123456@caomudai.com/"
browser = webdriver.Chrome()


def read_sentence():
    browser.get(auth_url)
    time.sleep(1)

    sel = Selector(text=browser.page_source)
    print(browser.title)
    sentence_list = sel.xpath("//div[@class='content']/ul/li/p/text()").extract()
    for sentence in sentence_list:
        print(sentence)
        # print(sentence.strip() + "\n")


if __name__ == '__main__':
    read_sentence()
