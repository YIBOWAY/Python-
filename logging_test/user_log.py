import logging
import os
import time


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


if __name__ == '__main__':
    user = Userlog()
    log = user.get_log()
    log.debug('test')
    user.close_handle()
