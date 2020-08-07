from scrapy import Selector
import requests

url = "http://caomudai.com/"
# auth_url = "http://admin:123456@caomudai.com/"


def read_sentence():
    req = requests.get(url)
    req.encoding = 'utf-8'
    res_text = req.text

    sel = Selector(text=res_text)
    sentence_list = sel.xpath("//div[@class='content']/ul/li/p/text()").extract()
    for sentence in sentence_list:
        print(sentence)
        # print(sentence.strip() + "\n")


if __name__ == '__main__':
    read_sentence()
