import re

info = "姓名：sunyb 生日：2000年11月20日 本科：2018年6月5日"
# print(re.findall("\d{4}",info))

# match_result = re.match(".*生日.*?(\d{4}).*本科.*?(\d{4})",info)  #加？取消*的贪婪模式，match只会一行行的匹配
# print(match_result.group(1))
# print(match_result.group(2))
#match是从字符串最开始的地方开始匹配
result = re.sub("\d{4}","2019",info)#替换
print(info)
print(result)
match_result = re.search("生日.*?(\d{4}).*本科.*?(\d{4})",info)  #查找
print(match_result.group(1))
print(match_result.group(2))

name = """
my name is
syb
"""
print(re.match(".*syb",name,re.DOTALL).group())  # DOTALL表示一直往下进行匹配