import os

import time
# 获取当前文件的上一层绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def time_change(str_time):
    timeStamp = str(str_time)[0:-3]
    timeStampInt = int(timeStamp)
    timeArray = time.localtime(timeStampInt)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime