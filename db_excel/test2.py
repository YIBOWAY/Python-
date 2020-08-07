import pandas as pd
import pymysql, openpyxl, os, xlsxwriter,xlrd
from xlutils.copy import copy
# 设定excel文件名称
# version = 'V1.4.6'
filename = 'foo.xls'
os.chdir('D:\\Test Project\\Python爬虫\\db_excel')
# 连接mysql数据库
settings = {"host": "222.223.239.147",
            "database": "imooc",
            "user": "root",
            "password": "Xinboway@803",
            "port": 3307,
            "charset": "utf8"}
db = pymysql.connect(host=settings['host'], database=settings['database'], user=settings['user'],
                     password=settings['password'], port=settings['port'], charset=settings['charset'])
# 追加到已有excel文件时，更改此处SQL条件
sql = 'select ename from employee where eno = 1005'
cursor = db.cursor()
count = cursor.execute(sql)
print(count)
results = cursor.fetchall()
print(results)
# 将SQL返回结果存储为dataFrame格式
# data = pd.read_sql(sql, db)
# # rownu为查询结果的条数
# rownu = data.index.stop

# 追加数据到已有excel文件中
def insertexcel():
    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheet_by_name("table_employee")
    sheet1 = copy(workbook)
    sheet2 = sheet1.get_sheet("table_employee")
    sheet2.write(14,0,u'%s'%results[0]) #定义位置
    os.remove(filename)# 移除原文件
    sheet1.save(filename) #保存新文件

# 新建excel文件中，并设置列表头格式
def newexcel():
    workbook = xlsxwriter.Workbook(filename)
    sheet = workbook.add_worksheet()
    sheet.set_column('A:A', 30)
    sheet.set_column('B:E', 11)
    sheet.set_column('F:F', 75)
    heading = list(data)
    headbold = workbook.add_format({'bold': True,
                                    'align': 'center',
                                    'border': 1,
                                    'bg_color': '#D3D3D3'})
    sheet.write_row('A1', heading, headbold)
    for i in range(0, rownu):
        sheet.write_row('A%s' % (i + 2), data.values[i])
    workbook.close()

# 判断文件是否存在并运行相应函数
if os.path.exists(filename):
    print('----文件已存在，将追加数据到%s----' % filename)
    insertexcel()
else:
    print('----文件不存在,将新建文件%s----' % filename)
    newexcel()

print('数据加载完毕!')