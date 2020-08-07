import os ,sys
import shutil

path = r'D:\testfolder'
path1 = r'E:\testfolder\testfolde'
# print ("目录为%s"%os.listdir(path=path))

# os.rename("D:\\testfolder\\text1.txt","D:\\testfolder\\test.txt")

# print("重命名成功")

# print("目录为：%s" %os.listdir(path=path))

# if os.path.exists(path):
#     print(path)
# else:
#     os.mkdir(path)
#     print("创建目录"+path+"成功")
# shutil.move("D:\\testfolder\\test.txt","D:\\testfolder\\testfolde")

# os.rename("D:\\testfolder\\test1.txt","D:\\testfolder\\test3.txt")
# os.rename("D:\\testfolder\\test2.txt","D:\\testfolder\\test4.txt")
if os.path.exists(path1):
    print(path1)
else:
    os.makedirs(path1)
    print("创建目录" + path1 + "成功")
sourcename = path
for filename in os.listdir(sourcename):
    print(filename)
    filepath = os.path.join(sourcename,filename)
    shutil.move(filepath,"D:\\testfolder\\testfolde\\testfold")

# shutil.move(path2+old_name+time1+houzhui,"D:\\testfolder\\testfolde\\testfold")
# shutil.move("D:\\testfolder\\test3.txt","D:\\testfolder\\testfolde\\testfold")
# shutil.move("D:\\testfolder\\test4.txt",path1)

print("移动文件夹成功")


