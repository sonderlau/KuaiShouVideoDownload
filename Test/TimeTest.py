import time
from datetime import datetime
if __name__ == '__main__':
    timestamp = 1628675403899 / 1000.0
    local = time.localtime(timestamp)
    str = time.strftime("%Y-%m-%d_%H-%M-%S", local)
    print(str)
    print(int(time.time() * 1000.0 ))
    print(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time())))
