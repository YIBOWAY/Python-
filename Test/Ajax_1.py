import requests
import logging_test
#*
# 分析Ajax请求
#模拟Ajax请求，属性，参数
# 返回json类型
logging_test.basicConfig(level=logging_test.INFO,
                         format='%(asctime)s - %(levelname)s: %(message)s')

INDEX_URL = 'https://dynamic1.scrape.cuiqingcai.com/api/movie/?limit={limit}&offset={offset}'


def scrape_api(url):
    logging_test.info('scraping %s...', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        logging_test.error('get invalid status code %s while scraping %s', response.status_code, url)
    except requests.RequestException:
        logging_test.error('error occurred while scraping %s', url, exc_info=True)


LIMIT = 10


def scrape_index(page):
    url = INDEX_URL.format(limit=LIMIT, offset=LIMIT * (page - 1))
    return scrape_api(url)


DETAIL_URL = 'https://dynamic1.scrape.cuiqingcai.com/api/movie/{id}'


def scrape_detail(id):
    url = DETAIL_URL.format(id=id)
    return scrape_api(url)


TOTAL_PAGE = 10


def main():
    for page in range(1, TOTAL_PAGE + 1):
        index_data = scrape_index(page)
        for item in index_data.get('results'):
            id = item.get('id')
            detail_data = scrape_detail(id)
            logging_test.info('detail data %s', detail_data)


main()
