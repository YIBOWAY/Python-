from selenium import webdriver
import pandas as pd
browser = webdriver.Chrome()
# 当测试好能够顺利爬取后，为加快爬取速度可设置无头模式，即不弹出浏览器
# 添加无头headlesss 1使用chrome headless,2使用PhantomJS
# 使用 PhantomJS 会警告高不建议使用phantomjs，建议chrome headless
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# browser = webdriver.Chrome(chrome_options=chrome_options)
# browser = webdriver.PhantomJS()
# browser.maximize_window()  # 最大化窗口,可以选择设置
lst = []
def get(url):
    browser.get(url)
    element = browser.find_element_by_css_selector('#dt_1')  # 定位表格，element是WebElement类型
    # 提取表格内容td
    td_content = element.find_elements_by_tag_name("td") # 进一步定位到表格内容所在的td节点
     # 存储为list
    for td in td_content:
        lst.append(td.text)
    print(lst) # 输出表格内容

def get_list(g_list):
    element = browser.find_element_by_css_selector('#dt_1')  # 定位表格，element是WebElement类型
    # 确定表格列数
    col = len(element.find_elements_by_css_selector('tr:nth-child(1) td'))
    # 通过定位一行td的数量，可获得表格的列数，然后将list拆分为对应列数的子list
    g_list= [g_list[i:i + col] for i in range(0, len(g_list), col)]
    df_table = pd.DataFrame(g_list)
    print(df_table)

if __name__ =='__main__':
    url = 'http://data.eastmoney.com/bbsj/201806/lrb.html'
    get(url)
    get_list(lst)