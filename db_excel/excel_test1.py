import xlwings as xw

app = xw.App(visible=True,add_book=False)
wb = app.books.open('foo.xls')
sht = wb.sheets[0]
rng = sht.range('A1:E14')
print(rng.value)